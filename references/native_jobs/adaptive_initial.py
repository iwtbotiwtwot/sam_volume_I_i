"""R1 follow-on selected from the completed lane01 native return."""
from pathlib import Path
import json
from build import Job, ROOT, BASE, DATA, scalar, matrix, cell, sha, save

RUN=ROOT/'GEN4/duck_gen6_local/runs/chapter1-lane01-20261015-01'
P=RUN/'workers/G6_01/tasks/r1_lane01_complete_source/RESULT.json'
D=json.loads(P.read_text())
assert D['status']=='COMPLETED' and D['gen6_execution']['status']=='PASSED'
j=Job('r1_lane01_initial_reference','Use actual R1 lane01 source/coupling to receive the signed initial hard-reference clock correlation and the concrete weighted field-form constant',extra=[Path(__file__),P,BASE/'derivation/DERIVATION_DRAFT.md'])
j.adopt('g',D['returned']['g']['value'],'Consume actual current-run signed lane01 coupling')
for name,source in [('M','M'),('Omega','actual_initial_rate'),('Delta','Delta'),('phi_plus','initial_S_phi_plus'),('phi_cross','initial_S_phi_cross'),('mu','mu'),('R','R')]:
    scalar(j,name,DATA['clock_outputs'][source]['entries'][0][0],'Exact retained coherent hard-clock operand '+source)
j.positive('M',1);j.positive('Omega',1);j.positive('phi_plus',1)
j.scale('two_g','g',1,2,'Signed original source-field incidence')
j.prod('two_g_phi','two_g' and matrix('two_g'),matrix('phi_plus'),'Signed plus-correlator clock correction')
j.solve('correlation_rate_shift',matrix('M'),matrix('two_g_phi'),'Joint correlation contribution to actual initial rate')
j.add('initial_rate',1,1,[('Delta',1),('correlation_rate_shift',1)],'Recover actual initial clock from the joint correlation')
j.add('initial_rate_reference_residual',1,1,[('initial_rate',1),('Omega',-1)],'Initial correlated actual rate closes on the true hard gap');j.assert_zero('initial_rate_reference_residual',1,1)
j.add('Delta_minus_Omega',1,1,[('Delta',1),('Omega',-1)],'Hard-reference shift with common true parameters')
j.prod('reference_numerator',matrix('Delta_minus_Omega'),matrix('M'),'Retain reference cancellation before interval comparison')
j.scale('reference_minus','reference_numerator',1,-1,'Signed plus-polarization reference numerator')
j.solve('reference_phi_plus',matrix('two_g'),matrix('reference_minus'),'Original algebraic reference plus correlator')
j.add('reference_correlator_residual',1,1,[('phi_plus',1),('reference_phi_plus',-1)],'Match the actual initial joint source-field correlator');j.assert_zero('reference_correlator_residual',1,1)
j.assert_zero('phi_cross',1,1)
j.scale('CB_squared','mu',1,2,'Concrete continuous form constant squared under the two-polarization normalization')
j.sqrt('CB','CB_squared',1)
j.scale('twoR','R',1,2,'Original finite weighted continuum norm denominator')
scalar(j,'one',1,'Unit normalization')
j.solve('inverse_twoR',matrix('twoR'),matrix('one'),'Model-specific weighted constant square 1/(2R)')
j.add('form_constant_residual',1,1,[('CB_squared',1),('inverse_twoR',-1)],'Weighted full-continuum constant normalization');j.assert_zero('form_constant_residual',1,1)
for k in ['M','Omega','Delta','phi_plus','phi_cross','correlation_rate_shift','initial_rate','initial_rate_reference_residual','reference_phi_plus','reference_correlator_residual','CB_squared','CB','form_constant_residual']:j.out(k,k)
task=j.make_task('G6_04',consumes=dict(lane01_source={'$result':'r1_lane01_complete_source','path':['returned','g']}))
save(BASE/'ops/ADAPTIVE_R1_TASK.json',task)
import sys
sys.path.insert(0,str(ROOT/'SAM_PROJECT/gen6_duck_t500/active_core'))
from sam_one_principle.adapter import validate
save(BASE/'ops/ADAPTIVE_R1_VALIDATION.json',dict(status='COMPILED_NO_SCIENCE',steps=len(j.steps),validation=validate(json.loads(Path(task['job_path']).read_text()))))
print(json.dumps(dict(status='COMPILED_NO_SCIENCE',steps=len(j.steps),task=str(BASE/'ops/ADAPTIVE_R1_TASK.json'))))
