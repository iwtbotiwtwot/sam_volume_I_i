"""Compile actual-R1 placement weights into the complete preparation account.

Importing this module emits no job and starts no science. The operator invokes
main only after reviewing the complete actual first-round outcome packet.
"""
from pathlib import Path
from copy import deepcopy
import json
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import Job, BASE, ROOT, DATA, scalar, matrix, cell, diag, wire, sha, save

RUN = ROOT / 'GEN4/duck_gen6_local/runs/chapter1-lane01-20261015-01'
WEIGHTS_KEY = 'r1_placement_spectral_weights'
PAIRS = [(a, b) for a in range(4) for b in range(a + 1, 4)]


def actual_weights(run):
    receipt = run / 'workers/G6_02/tasks' / WEIGHTS_KEY / 'RESULT.json'
    envelope = run / 'native_returns' / (WEIGHTS_KEY + '.json')
    reference = json.loads(envelope.read_text())
    expected = reference.get('record_file_sha256', reference['receipt_sha256'])
    if sha(receipt) != expected:
        raise ValueError('Actual R1 placement receipt differs from its envelope')
    result = json.loads(receipt.read_text())
    if result.get('status') != 'COMPLETED' or result.get('gen6_execution', {}).get('status') != 'PASSED':
        raise ValueError('Placement composition requires the completed actual R1 result')
    trace = next(row for row in result['gen6_execution']['trace'] if row['id'] == 'weights')
    output = Path(result['gen6_execution_path']) / trace['output']
    if sha(output) != trace['output_sha256']:
        raise ValueError('Actual R1 placement-weight native output differs')
    return deepcopy(result['returned']['weights']['value']), [receipt, envelope, output]


def build(run=RUN):
    weights, receipt_files = actual_weights(Path(run))
    j = Job('r2_placement_population_energy',
        'Receive actual R1 placement spectral weights and reconstruct all four diagonal and six symmetric-pair populations, complete reference energy and original-basis calibration variance',
        extra=[Path(__file__), *receipt_files])
    j.binding.update(
        actual_R1_finding='All four original-placement spectral weights are strictly positive; norm, first moment756 and second moment583952 close in native arithmetic',
        source_receiving='Actual current-run weights receipt plus authenticated exact original-placement Hpair/D/C and source-root inputs',
        population_scope='For the identical product placement |e0> tensor |e0>: four p_a squared diagonal populations and six2p_a p_b symmetric-pair populations; antisymmetric pair population zero',
        coherences='The pure placement state and all its spectral coherences remain; the weight table is only the diagonal account sufficient for this block-diagonal source energy',
        original_placement_current_scope='D00=C00=0 are expectation values, not claims that the currents annihilate the placement ket',
        consumed_native_receipts=[dict(key=WEIGHTS_KEY, path=str(receipt_files[0]), sha256=sha(receipt_files[0]))])
    j.adopt('weights', weights, 'Receive actual R1 projector expectations without midpoint replacement')
    j.adopt('q', DATA['q'], 'Retain all four certified source roots in their original spectral order')
    for name in ['Hpair', 'D', 'C']:
        j.adopt(name, DATA['source_outputs'][name], 'Retain complete original-placement sixteen-dimensional ' + name)
    j.adopt('Eref', DATA['Eref'], 'Original placement reference energy573049')
    j.adopt('epsilon', DATA['epsilon'], 'Retained capacity-normalized source receiving coefficient')
    scalar(j, 'one', 1, 'Exact full-source product-state norm')

    j.prod('diagonal_populations', matrix('weights'), matrix('weights'),
           'Four same-root populations p_a squared in the identical product preparation')
    j.admit('pair_p_a', diag([cell('weights', a, a) for a, b in PAIRS])['entries'],
            'First projector weight for each original ordered a<b pair')
    j.admit('pair_p_b', diag([cell('weights', b, b) for a, b in PAIRS])['entries'],
            'Second projector weight for each original ordered a<b pair')
    j.prod('pair_weight_products', matrix('pair_p_a'), matrix('pair_p_b'),
           'Retain both equal ordered-product amplitudes on every pair')
    j.scale('pair_populations', 'pair_weight_products', 6, 2,
            'Six symmetric-pair populations2p_a p_b; retain their coherent symmetric combination')
    j.positive('diagonal_populations', 4)
    j.positive('pair_populations', 6)
    j.prod('diagonal_population_sum', wire([[1] * 4]),
           wire([[cell('diagonal_populations', i, i)] for i in range(4)]),
           'Account for every same-root spectral population')
    j.prod('pair_population_sum', wire([[1] * 6]),
           wire([[cell('pair_populations', i, i)] for i in range(6)]),
           'Account for every unequal-root symmetric spectral population')
    j.add('total_population', 1, 1, [('diagonal_population_sum', 1), ('pair_population_sum', 1)],
          'Complete placement product-state population across four diagonal and six paired sectors')
    j.add('population_normalization_residual', 1, 1, [('total_population', 1), ('one', -1)],
          'Exact interval closure of the complete product-state norm')
    j.assert_zero('population_normalization_residual', 1, 1)

    j.admit('I4', diag([1] * 4)['entries'], 'All four same-root source sectors')
    j.add('one_plus_q', 4, 4, [('I4', 1), ('q', 1)], 'Complete same-root source energy factor1+q_a')
    j.prod('diagonal_energies', matrix('one_plus_q'), matrix('one_plus_q'),
           'Unforced same-root source energies(1+q_a) squared with full even reference')
    j.admit('pair_q_a', diag([cell('q', a, a) for a, b in PAIRS])['entries'],
            'First root identity in every unequal-root symmetric pair')
    j.admit('pair_q_b', diag([cell('q', b, b) for a, b in PAIRS])['entries'],
            'Second root identity in every unequal-root symmetric pair')
    j.prod('pair_q_product', matrix('pair_q_a'), matrix('pair_q_b'),
           'Complete pair-source product contribution')
    j.admit('I6', diag([1] * 6)['entries'], 'Six symmetric source sectors with exchange eigenvalue+1')
    j.add('pair_energies', 6, 6,
          [('I6', 1), ('pair_q_a', 1), ('pair_q_b', 1), ('pair_q_product', 1)],
          'Full symmetric-pair energies1+q_a+q_b+q_a q_b, including every commuting offset')
    j.prod('diagonal_energy_contributions', matrix('diagonal_populations'), matrix('diagonal_energies'),
           'All four population-weighted diagonal source energies')
    j.prod('pair_energy_contributions', matrix('pair_populations'), matrix('pair_energies'),
           'All six population-weighted symmetric-pair source energies')
    j.prod('diagonal_energy_sum', wire([[1] * 4]),
           wire([[cell('diagonal_energy_contributions', i, i)] for i in range(4)]),
           'Complete same-root contribution to calibration energy')
    j.prod('pair_energy_sum', wire([[1] * 6]),
           wire([[cell('pair_energy_contributions', i, i)] for i in range(6)]),
           'Complete symmetric-pair contribution to calibration energy')
    j.add('total_spectral_energy', 1, 1, [('diagonal_energy_sum', 1), ('pair_energy_sum', 1)],
          'Reconstruct the complete placement calibration energy from the actual spectral weights')
    j.add('spectral_energy_residual', 1, 1, [('total_spectral_energy', 1), ('Eref', -1)],
          'Spectral reconstruction closes on the original573049 source reference')
    j.assert_zero('spectral_energy_residual', 1, 1)
    j.prod('normalized_total_energy', matrix('epsilon'), matrix('total_spectral_energy'),
           'Receive the complete calibration energy through the declared epsilon chart')
    j.add('normalized_energy_residual', 1, 1, [('normalized_total_energy', 1), ('one', -1)],
          'Normalized complete placement reference energy closes on one')
    j.assert_zero('normalized_energy_residual', 1, 1)

    ket = [[int(i == 0)] for i in range(16)]
    j.admit('placement_ket', ket, 'Exact labelled original-placement product ket |e0,e0> in the full16 carrier')
    j.op('placement_bra', 'GEN3_COMPLEX_ADJOINT', dict(matrix=matrix('placement_ket')),
         'Preserve the full labelled placement-state bra')
    j.prod('placement_density', matrix('placement_ket'), matrix('placement_bra'),
           'Retain the complete pure placement state; no spectral dephasing is performed')
    for name in ['Hpair', 'D', 'C']:
        j.prod(name + '_placement_action', matrix(name), matrix('placement_ket'),
               'Apply full original-placement ' + name + ' to the calibration ket')
        j.prod(name + '_placement_expectation', matrix('placement_bra'), matrix(name + '_placement_action'),
               'Full original-basis calibration expectation of ' + name)
    j.add('placement_energy_residual', 1, 1, [('Hpair_placement_expectation', 1), ('Eref', -1)],
          'Full16 original-placement expectation closes on573049')
    j.assert_zero('placement_energy_residual', 1, 1)
    j.assert_zero('D_placement_expectation', 1, 1)
    j.assert_zero('C_placement_expectation', 1, 1)
    j.add('spectral_placement_energy_closure', 1, 1,
          [('total_spectral_energy', 1), ('Hpair_placement_expectation', -1)],
          'Actual spectral population energy and complete placement-basis energy agree')
    j.assert_zero('spectral_placement_energy_closure', 1, 1)
    j.prod('Hpair_squared', matrix('Hpair'), matrix('Hpair'),
           'Complete source energy square, retaining every original placement component')
    j.prod('Hpair_squared_placement_action', matrix('Hpair_squared'), matrix('placement_ket'),
           'Retain complete second source-energy moment of the calibration state')
    j.prod('placement_energy_second_moment', matrix('placement_bra'), matrix('Hpair_squared_placement_action'),
           'Full sixteen-dimensional calibration expectation of Hpair squared')
    j.prod('Eref_squared', matrix('Eref'), matrix('Eref'), 'Square of the exact calibration mean energy')
    j.add('placement_energy_variance', 1, 1,
          [('placement_energy_second_moment', 1), ('Eref_squared', -1)],
          'Positive source-energy variance distinguishes calibration from a stationary source eigenstate')
    j.positive('placement_energy_variance', 1)

    readouts = [
        'weights', 'q', 'Hpair', 'D', 'C', 'Eref', 'epsilon',
        'diagonal_populations', 'pair_populations', 'diagonal_population_sum',
        'pair_population_sum', 'total_population', 'population_normalization_residual',
        'diagonal_energies', 'pair_energies', 'diagonal_energy_contributions',
        'pair_energy_contributions', 'diagonal_energy_sum', 'pair_energy_sum',
        'total_spectral_energy', 'spectral_energy_residual', 'normalized_total_energy',
        'normalized_energy_residual', 'placement_ket', 'placement_bra', 'placement_density',
        'Hpair_placement_expectation', 'D_placement_expectation', 'C_placement_expectation',
        'placement_energy_residual', 'spectral_placement_energy_closure',
        'placement_energy_second_moment', 'Eref_squared', 'placement_energy_variance']
    for name in readouts:
        j.out(name, name)
    j.outputs['preparation_account'] = dict(status='ANALYTIC_CONTRACT', value=dict(
        diagonal_sectors=[[a, a] for a in range(4)], paired_sectors=[list(pair) for pair in PAIRS],
        diagonal_population='p_a squared', symmetric_pair_population='2p_a p_b',
        antisymmetric_pair_population='0 for this identical product placement',
        diagonal_energy='(1+q_a)^2', symmetric_pair_energy='1+q_a+q_b+q_a q_b',
        retained_state='Pure |e0,e0><e0,e0| in the original placement basis; all spectral coherences retained',
        table_scope='Diagonal spectral account sufficient for block-diagonal source energy; not a replacement density matrix',
        calibration='Mean source energy573049, normalized mean1, positive source-energy variance',
        currents='D00=C00=0 are expectations; neither current is declared to annihilate the placement ket',
        hard_clock_preparation='Separate coherent exact hard charge0/1 preparation plus common soft vacuum'))
    return j


def main():
    j = build()
    task = j.make_task('G6_05', target='PLACEMENT_PREPARATION',
                       consumes={'placement_weights': {'$result': WEIGHTS_KEY, 'path': ['key']}})
    sys.path.insert(0, str(ROOT / 'SAM_PROJECT/gen6_duck_t500/active_core'))
    from sam_one_principle.adapter import validate
    validation = validate(json.loads(Path(task['job_path']).read_text()))
    save(BASE / 'ops/R2_PREPARATION_TASK.json', task)
    save(BASE / 'ops/R2_PREPARATION_VALIDATION.json', dict(
        status='COMPILED_NO_SCIENCE', validation=validation, steps=len(j.steps),
        readouts=list(j.outputs), compiler=dict(path=str(Path(__file__).resolve()), sha256=sha(__file__)),
        actual_R1_receipt=j.binding['consumed_native_receipts']))
    print(json.dumps(dict(status='COMPILED_NO_SCIENCE', steps=len(j.steps),
                         readouts=list(j.outputs), task=str(BASE / 'ops/R2_PREPARATION_TASK.json'))))


if __name__ == '__main__':
    main()
