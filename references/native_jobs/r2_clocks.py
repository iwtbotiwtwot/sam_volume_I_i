"""Compile R2 only from the actual new uniform-clock findings."""
from pathlib import Path
from fractions import Fraction
import json,sys
from build import Job, ROOT, BASE, DATA, scalar, matrix, cell, wire, diag, eye, sha, save

RUN=ROOT/'GEN4/duck_gen6_local/runs/chapter1-lane01-20261015-01'
P=RUN/'workers/G6_03/tasks/r1_uniform_whole_cycle_clocks/RESULT.json'
D=json.loads(P.read_text())
assert D['status']=='COMPLETED' and D['gen6_execution']['status']=='PASSED'
V={k:v['value'] for k,v in D['returned'].items() if isinstance(v,dict) and 'value' in v}
ELIGIBLE=[i for i in range(6) if Fraction(V['uniform_rate_lower']['entries'][i][i]['re']['lower'])>0]
PAIRS=[(a,b) for a in range(4) for b in range(a+1,4)]

def inverse_job():
    j=Job('r2_uniform_inverse_action','Receive actual uniformly positive R1 lanes into a common instantaneous phase inverse and complete dependent lane-action coefficient family',extra=[Path(__file__),P,BASE/'derivation/DERIVATION_DRAFT.md'])
    j.binding.update(selected_lanes=[PAIRS[i] for i in ELIGIBLE],coefficient_dependency='Every marginal coefficient uses the SAME underlying actual nu(t); no independent coefficient sampling',phase_scope='Whole retained cycle; reciprocal is instantaneous dt/dgamma, not a finite-window average')
    n=len(ELIGIBLE)
    assert n>0
    entries=[dict(re=dict(lower=V['uniform_rate_lower']['entries'][i][i]['re']['lower'],upper=V['uniform_rate_upper']['entries'][i][i]['re']['upper']),im='0') for i in ELIGIBLE]
    j.admit('nu',diag(entries)['entries'],'Actual uniform pointwise rate interval selected by native positive lower bounds');j.positive('nu',n)
    j.solve('inverse_rate',matrix('nu'),eye(n),'Instantaneous positive phase-coordinate inverse dt/dgamma');j.positive('inverse_rate',n)
    for k,name in [('epsilon','epsilon'),('g','g'),('counterterm','counterterm')]:
        j.admit(k,diag([DATA['clock_outputs'][name]['entries'][i][i] for i in ELIGIBLE])['entries'],'Retained complete lane coefficient '+name)
    j.admit('even_energy',diag([DATA['source_outputs']['even_energy']['entries'][i][i] for i in ELIGIBLE])['entries'],'Keep commuting source energy in the phase action')
    j.scale('field_kinetic','nu',n,'1/5','Velocity transformation gives kappa nu/4=nu/5')
    j.scale('field_gradient','inverse_rate',n,'-1/5','Same underlying actual phase rate in radial gradient coefficient')
    j.scale('field_angular','inverse_rate',n,'-6/5','Same underlying actual phase rate in angular coefficient')
    for name,source,sign in [('source_even','even_energy',-1),('source_exchange','epsilon',-1),('boundary_interaction','g',1),('both_counterterms','counterterm',-1)]:
        j.prod(name+'_raw',matrix(source),matrix('inverse_rate'),'Complete lane '+name+' receives the common instantaneous inverse')
        j.scale(name,name+'_raw',n,sign,'Retain action sign and both real-polarization payments')
    j.prod('inverse_closure',matrix('nu'),matrix('inverse_rate'),'Native phase-inverse closure')
    j.admit('I',eye(n)['entries'],'Selected lane identities')
    j.add('inverse_residual',n,n,[('inverse_closure',1),('I',-1)],'Retain all inverse residual entries');j.assert_zero('inverse_residual',n,n)
    for k in ['nu','inverse_rate','field_kinetic','field_gradient','field_angular','source_even','source_exchange','boundary_interaction','both_counterterms','inverse_residual']:j.out(k,k)
    j.outputs['coefficient_contract']=dict(status='ANALYTIC_CONTRACT',value=dict(pairs=[PAIRS[i] for i in ELIGIBLE],same_underlying_nu=True,Berry_one_form='unchanged',retained_velocity='phi_tau_dot=nu*partial_gamma(phi)',source_even_operator='Scalar only within each stated lane; full source complement retained'))
    return j

def centered_job():
    j=Job('r2_centered_uniform_budgets','Use the actual R1 whole-cycle field form to obtain conservative centered correlator enclosures and explicit remaining uniform accuracy targets for all six lanes',extra=[Path(__file__),P,BASE/'derivation/DERIVATION_DRAFT.md',BASE/'derivation/DOMAIN_SUPPLEMENT.md'])
    j.binding.update(reference='Exact coherent hard branches evolved with hard Hamiltonian plus free soft field and scalar soft counterterm; same field form realization',error_scope='sup over0<=t<=T; triangle centered bound from whole-field energy and actual hard-reference expectation',weighted_distance_scope='Budget only, not an achieved propagated state-distance')
    for k in ['Delta','g','M_lower','M_upper','actual_initial_rate','mu','CYCLE_E']:
        j.adopt(k,DATA['clock_outputs'][k],'Reuse exact retained clock input '+k)
    j.adopt('Ef_T',V['Ef_T'],'Use actual R1 uniform whole-field energy enclosure')
    def endpoint(k,source,side):
        j.admit(k,diag([dict(re=dict(lower=DATA['clock_outputs'][source]['entries'][i][i]['re'][side],upper=DATA['clock_outputs'][source]['entries'][i][i]['re'][side]),im='0') for i in range(6)])['entries'],'Conservative directed '+side+' endpoint of '+source)
    endpoint('Omega_lo','actual_initial_rate','lower');endpoint('M_lo','M_lower','lower');endpoint('M_hi','M_upper','upper');endpoint('E_up','CYCLE_E','upper')
    j.scale('g_abs','g',6,-1,'Retain signed negative g and its positive magnitude');j.positive('g_abs',6)
    j.admit('g_abs_lo',diag([dict(re=dict(lower=DATA['clock_outputs']['g']['entries'][i][i]['re']['upper'],upper=DATA['clock_outputs']['g']['entries'][i][i]['re']['upper']),im='0') for i in range(6)])['entries'],'Receive signed upper endpoints before magnitude conversion')
    j.scale('G_lo','g_abs_lo',6,-1,'Positive lower magnitude of negative signed coupling')
    j.admit('g_abs_up',diag([dict(re=dict(lower=DATA['clock_outputs']['g']['entries'][i][i]['re']['lower'],upper=DATA['clock_outputs']['g']['entries'][i][i]['re']['lower']),im='0') for i in range(6)])['entries'],'Receive signed lower endpoints before magnitude conversion')
    j.scale('G_up','g_abs_up',6,-1,'Conservative upper magnitude, retaining signed source in the exact identity')
    j.prod('OmegaM','Omega_lo' and matrix('Omega_lo'),matrix('M_lo'),'Common-parameter reference budget before absolute-value losses')
    j.prod('DeltaE',matrix('Delta'),matrix('E_up'),'Uniform current-error payment at T')
    j.add('free_margin',6,6,[('OmegaM',1),('DeltaE',-1)],'Centered positive correlator-error margin');j.positive('free_margin',6)
    j.scale('two_G_up','G_up',6,2,'Full signed-source magnitude payment for conservative budget')
    j.solve('W_budget',matrix('two_G_up'),matrix('free_margin'),'Uniform sufficient target Wsup < budget');j.positive('W_budget',6)
    j.prod('muEf',matrix('mu'),matrix('Ef_T'),'Complete field energy-form current norm')
    j.sqrt('sqrt_muEf','muEf',6)
    j.scale('actual_w_bound','sqrt_muEf',6,2,'Valid whole-field joint-correlator magnitude bound')
    j.add('reference_gap_shift',6,6,[('Delta',1),('Omega_lo',-1)],'Conservative true hard-reference gap shift')
    j.prod('reference_numerator',matrix('reference_gap_shift'),matrix('M_hi'),'Conservative hard-reference joint-correlator numerator')
    j.scale('two_G_lo','G_lo',6,2,'Positive lower denominator for reference magnitude')
    j.solve('reference_w_bound',matrix('two_G_lo'),matrix('reference_numerator'),'Bound actual hard-reference expectation, with common state/field realization')
    j.add('W_coarse',6,6,[('actual_w_bound',1),('reference_w_bound',1)],'Achieved conservative uniform centered error by triangle inequality')
    j.prod('coarse_payment',matrix('two_G_up'),matrix('W_coarse'),'Complete conservative centered-correlator payment')
    j.add('centered_margin',6,6,[('free_margin',1),('coarse_payment',-1)],'Retain every centered margin, including inconclusive lanes')
    j.solve('coarse_to_budget',matrix('W_budget'),matrix('W_coarse'),'Quantify remaining improvement needed for the uniform centered sufficient test')
    j.scale('CB_squared','mu',6,2,'Model-specific weighted continuous field-form constant squared')
    j.sqrt('CB','CB_squared',6)
    j.solve('weighted_trace_budget',matrix('CB'),matrix('W_budget'),'Sufficient weighted trace-distance target; propagated distance remains uncomputed')
    for k in ['Omega_lo','M_lo','E_up','G_lo','G_up','free_margin','W_budget','actual_w_bound','reference_w_bound','W_coarse','centered_margin','coarse_to_budget','CB','weighted_trace_budget']:j.out(k,k)
    j.outputs['centered_contract']=dict(status='ANALYTIC_CONTRACT',value=dict(time_interval='0<=t<=T=time_CYCLE',reference_mismatch='Zero for the explicitly identified coherent hard reference in the same weighted-form realization',sharper_correlator_propagation='not supplied; W_coarse uses the triangle energy-form bound',weighted_state_distance='not calculated; weighted_trace_budget is a target',all_six_lanes_retained=True))
    return j

def main():
    tasks=[];checks=[]
    for j,lane,target in [(inverse_job(),'G6_06','UNIFORM_CLOCK'),(centered_job(),'G6_07','CENTERED_REFINEMENT')]:
        task=j.make_task(lane,target,consumes=dict(uniform_clock={'$result':'r1_uniform_whole_cycle_clocks','path':['returned','uniform_rate_lower']}))
        sys.path.insert(0,str(ROOT/'SAM_PROJECT/gen6_duck_t500/active_core'))
        from sam_one_principle.adapter import validate
        checks.append(dict(key=j.key,steps=len(j.steps),validation=validate(json.loads(Path(task['job_path']).read_text()))));tasks.append(task)
    save(BASE/'ops/R2_CLOCK_TASKS.json',tasks);save(BASE/'ops/R2_CLOCK_VALIDATION.json',checks)
    print(json.dumps(dict(status='COMPILED_NO_SCIENCE',eligible_pairs=[PAIRS[i] for i in ELIGIBLE],tasks=len(tasks),steps=sum(c['steps'] for c in checks))))

if __name__=='__main__':main()
