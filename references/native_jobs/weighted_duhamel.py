"""New R2 weighted soft-reference propagation calculation.

Proposed form derivation: A=1+Hf <=2B<=4A for B=Hred+epsilon+c+1/2,
provided 2epsilon+3c+1/2<=2. Thus full evolution has A-norm <=2.
Reference soft vacuum gives ||A^1/2 Vsoft psi_ref||^2 <=
2g^2 vsoft(1+Ef_T+lambda). Duhamel and CB=sqrt(2mu) give
Wsup <=8|g|T sqrt(mu vsoft(1+Ef_T)(1+Ef_T+lambda)).
The companion analytical derivation determines the theorem's scope.
"""
from pathlib import Path
import json,sys
from build import Job,ROOT,BASE,DATA,scalar,matrix,cell,diag,eye,sha,save
RUN=ROOT/'GEN4/duck_gen6_local/runs/chapter1-lane01-20261015-01'
P=RUN/'workers/G6_03/tasks/r1_uniform_whole_cycle_clocks/RESULT.json'
U=json.loads(P.read_text());assert U['status']=='COMPLETED'
j=Job('r2_weighted_soft_duhamel','Evaluate the newly derived energy-weighted soft Duhamel certificate in all six lanes; certify actual centered margins and phase inverses when its explicit form/reference hypotheses hold',extra=[Path(__file__),P,BASE/'derivation/DOMAIN_SUPPLEMENT.md'])
j.binding.update(new_method='Energy-weighted Duhamel comparison to exact coherent hard branches times soft vacuum; full-field form dynamics; both helicities and exact soft scalar counterterm',theorem_status='New analytical construction; numerical intervals pay its explicit scalar bounds; mathematical review retained separately',propagation_interval='0<=t<=T=time_CYCLE')
for k in ['epsilon','Delta','g','counterterm','mu','vsoft','time_CYCLE','M_lower','M_upper','actual_initial_rate','CYCLE_E']:
    j.adopt(k,DATA['clock_outputs'][k],'Exact retained full-continuum source operand '+k)
j.adopt('Ef_T',U['returned']['Ef_T']['value'],'Use the actual native R1 uniform field-energy ceiling for actual and hard reference')
j.admit('I',eye(6)['entries'],'All six driven lanes')
j.scale('g_abs','g',6,-1,'Signed negative source coupling magnitude');j.positive('g_abs',6)
j.scale('lambda','Delta',6,64,'Same hard-soft preparation split')
j.scale('two_epsilon','epsilon',6,2,'Bounded lane source contribution')
j.scale('three_c','counterterm',6,3,'Complete square-form comparison payment')
j.add('norm_comparison_margin',6,6,[('I','3/2'),('two_epsilon',-1),('three_c',-1)],'Certify B<=2A for full two-polarization Hamiltonian');j.positive('norm_comparison_margin',6)
j.add('A_energy','I' and 6,6,[('I',1),('Ef_T',1)],'Bound both actual and reference A-norm squares')
j.add('creation_energy',6,6,[('A_energy',1),('lambda',1)],'Pay created soft-photon energy using omega<=lambda')
j.prod('mu_vsoft',matrix('mu'),matrix('vsoft'),'Finite weighted full-field norm times complete soft vacuum norm')
j.prod('energy_product',matrix('A_energy'),matrix('creation_energy'),'Both state norms and created-soft energy retained')
j.prod('weighted_kernel',matrix('mu_vsoft'),matrix('energy_product'),'Energy-weighted Duhamel kernel')
j.sqrt('weighted_kernel_root','weighted_kernel',6)
j.prod('gT',matrix('g_abs'),matrix('time_CYCLE'),'Signed source magnitude through the full retained time')
j.prod('W_raw',matrix('gT'),matrix('weighted_kernel_root'),'All-time soft-reference comparison before fixed norm factors')
j.scale('W_duhamel','W_raw',6,8,'Pay full propagation norm2, two state norms, both polarizations and CB=sqrt2mu');j.positive('W_duhamel',6)
def endpoint(k,name,side):
    j.admit(k,diag([dict(re=dict(lower=DATA['clock_outputs'][name]['entries'][i][i]['re'][side],upper=DATA['clock_outputs'][name]['entries'][i][i]['re'][side]),im='0') for i in range(6)])['entries'],'Directed conservative '+side+' endpoint of '+name)
endpoint('Omega_lo','actual_initial_rate','lower');endpoint('Omega_hi','actual_initial_rate','upper');endpoint('M_lo','M_lower','lower');endpoint('E_up','CYCLE_E','upper')
j.prod('OmegaM',matrix('Omega_lo'),matrix('M_lo'),'Preserve exact centered reference before interval separation')
j.prod('DeltaE',matrix('Delta'),matrix('E_up'),'Uniform current error payment')
j.prod('gW',matrix('g_abs'),matrix('W_duhamel'),'Full centered correlated-field error payment')
j.scale('two_gW','gW',6,2,'Signed equation correlation factor2')
j.add('centered_margin',6,6,[('OmegaM',1),('DeltaE',-1),('two_gW',-1)],'All six centered positivity margins from weighted propagation');j.positive('centered_margin',6)
j.add('gap_shift',6,6,[('Delta',1),('Omega_lo',-1)],'Conservative common hard-reference gap shift')
j.prod('gap_E',matrix('gap_shift'),matrix('E_up'),'Reference-centered current-error contribution')
j.add('rate_error_num',6,6,[('gap_E',1),('two_gW',1)],'Complete centered exact-rate error numerator')
j.add('amplitude_lower',6,6,[('M_lo',1),('E_up',-1)],'Uniform nonzero current amplitude');j.positive('amplitude_lower',6)
j.solve('centered_rate_error',matrix('amplitude_lower'),matrix('rate_error_num'),'Uniform actual rate error around the true hard gap')
j.add('rate_lower',6,6,[('Omega_lo',1),('centered_rate_error',-1)],'All six uniform actual phase-rate lower endpoints');j.positive('rate_lower',6)
j.add('rate_upper',6,6,[('Omega_hi',1),('centered_rate_error',1)],'All six uniform actual phase-rate upper endpoints')
j.admit('rate_interval',diag([dict(re=dict(lower={'$step':'rate_lower','path':['result','output','matrix','entries',i,i,'re','lower']},upper={'$step':'rate_upper','path':['result','output','matrix','entries',i,i,'re','upper']}),im='0') for i in range(6)])['entries'],'Receive the complete uniform actual-rate enclosure')
j.solve('inverse_rate',matrix('rate_interval'),eye(6),'Uniformly eligible instantaneous phase inverse on all six lanes')
j.scale('field_kinetic','rate_interval',6,'1/5','Same actual rate, kinetic velocity Jacobian retained')
j.scale('field_gradient','inverse_rate',6,'-1/5','Same actual rate in full gradient coefficient')
j.scale('field_angular','inverse_rate',6,'-6/5','Same actual rate in angular coefficient')
for k in ['norm_comparison_margin','A_energy','creation_energy','W_duhamel','Omega_lo','Omega_hi','M_lo','E_up','centered_margin','amplitude_lower','centered_rate_error','rate_lower','rate_upper','rate_interval','inverse_rate','field_kinetic','field_gradient','field_angular']:j.out(k,k)
j.outputs['propagation_contract']=dict(status='ANALYTIC_CONTRACT',value=dict(full_field_form=True,soft_reference_vacuum=True,soft_counterterm='Exact common scalar retained in both Hamiltonians, so difference is only soft linear interaction',state_norm_propagation='A<=2B<=4A implies full propagator A-norm<=2',soft_energy='m1soft<=lambda*vsoft',bound='Wsup<=8|g|T sqrt(mu vsoft(1+Ef_T)(1+Ef_T+lambda))',reference_mismatch='Zero in the stated exact hard reference',finite_photon_cutoff=False,rotating_wave=False,all_six_lanes=True))
t=j.make_task('G6_08','CENTERED_REFINEMENT',consumes=dict(uniform_field={'$result':'r1_uniform_whole_cycle_clocks','path':['returned','Ef_T']},prior_centered_budget={'$result':'r2_centered_uniform_budgets','path':['returned','W_budget']}))
save(BASE/'ops/WEIGHTED_DUHAMEL_TASK.json',t)
sys.path.insert(0,str(ROOT/'SAM_PROJECT/gen6_duck_t500/active_core'))
from sam_one_principle.adapter import validate
save(BASE/'ops/WEIGHTED_DUHAMEL_VALIDATION.json',dict(status='COMPILED_NO_SCIENCE',steps=len(j.steps),validation=validate(json.loads(Path(t['job_path']).read_text()))))
print(json.dumps(dict(status='COMPILED_NO_SCIENCE',steps=len(j.steps),task=str(BASE/'ops/WEIGHTED_DUHAMEL_TASK.json'))))
