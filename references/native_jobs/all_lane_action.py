"""R2 consequence selected from actual weighted-propagation certificates."""
from pathlib import Path
import json,sys
from build import Job,ROOT,BASE,DATA,matrix,eye,sha,save
RUN=ROOT/'GEN4/duck_gen6_local/runs/chapter1-lane01-20261015-01'
P=RUN/'workers/G6_08/tasks/r2_weighted_soft_duhamel/RESULT.json'
D=json.loads(P.read_text());assert D['status']=='COMPLETED' and D['gen6_execution']['status']=='PASSED'
j=Job('r2_all_lane_action_coefficients','Receive actual weighted-Duhamel all-six clock certificates into complete dependent phase-action coefficients and strict uniform delay checks',extra=[Path(__file__),P,BASE/'derivation/DOMAIN_SUPPLEMENT.md'])
j.binding.update(phase_scope='All six lanes, whole retained cycle',coefficient_dependency='Same underlying actual nu in every coefficient; intervals are marginal enclosures of this dependent family')
for k,name in [('nu','rate_interval'),('inverse_rate','inverse_rate'),('rate_upper','rate_upper')]:j.adopt(k,D['returned'][name]['value'],'Actual completed weighted-propagation '+name)
for k in ['epsilon','g','counterterm','Delta']:j.adopt(k,DATA['clock_outputs'][k],'Exact complete lane coefficient '+k)
j.adopt('even_energy',DATA['source_outputs']['even_energy'],'Retain every commuting even energy and sector-relative phase')
j.add('slower_margin',6,6,[('Delta',1),('rate_upper',-1)],'All six actual uniform upper rates lie strictly below the bare gap');j.positive('slower_margin',6)
j.scale('field_kinetic','nu',6,'1/5','Complete kinetic velocity Jacobian')
j.scale('field_gradient','inverse_rate',6,'-1/5','Common actual inverse phase rate')
j.scale('field_angular','inverse_rate',6,'-6/5','Complete quadrupole angular payment')
for k,src,sign in [('source_even','even_energy',-1),('source_exchange','epsilon',-1),('boundary_interaction','g',1),('both_counterterms','counterterm',-1)]:
    j.prod(k+'_raw',matrix(src),matrix('inverse_rate'),'Complete '+k+' through the same actual rate')
    j.scale(k,k+'_raw',6,sign,'Retain source sign and both polarization accounts')
j.prod('inverse_closure',matrix('nu'),matrix('inverse_rate'),'Actual phase inverse closure on all six lanes')
j.admit('I',eye(6)['entries'],'All six source-lane identities')
j.add('inverse_residual',6,6,[('inverse_closure',1),('I',-1)],'Native full inverse residual');j.assert_zero('inverse_residual',6,6)
for k in ['nu','inverse_rate','slower_margin','field_kinetic','field_gradient','field_angular','source_even','source_exchange','boundary_interaction','both_counterterms','inverse_residual']:j.out(k,k)
j.outputs['dependent_family']=dict(status='ANALYTIC_CONTRACT',value=dict(pairs=[[a,b] for a in range(4) for b in range(a+1,4)],same_actual_nu=True,kinetic_velocity='phi_tau_dot=nu partial_gamma(phi)',Berry_one_form='unchanged',all_time='0<=t<=T=time_CYCLE',both_counterterms=True,even_energy_retained=True))
t=j.make_task('G6_09','UNIFORM_CLOCK',consumes=dict(weighted_propagation={'$result':'r2_weighted_soft_duhamel','path':['returned','rate_interval']}))
save(BASE/'ops/ALL_LANE_ACTION_TASK.json',t)
sys.path.insert(0,str(ROOT/'SAM_PROJECT/gen6_duck_t500/active_core'))
from sam_one_principle.adapter import validate
save(BASE/'ops/ALL_LANE_ACTION_VALIDATION.json',dict(status='COMPILED_NO_SCIENCE',steps=len(j.steps),validation=validate(json.loads(Path(t['job_path']).read_text()))))
print(json.dumps(dict(status='COMPILED_NO_SCIENCE',steps=len(j.steps))))
