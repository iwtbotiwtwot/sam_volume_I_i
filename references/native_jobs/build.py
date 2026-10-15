"""Assemble source-bound native jobs; importing/building performs no science."""
from pathlib import Path
from copy import deepcopy
import argparse
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'GEN4/duck_source_action1_20261014'))
from programs import Job as Prior, wire, eye, diag, matrix, cell, sha, save
INPUT = BASE / 'sources/EXACT_INPUTS.json'
MANIFEST = BASE / 'sources/SOURCE_MANIFEST.json'
DATA = json.loads(INPUT.read_text())
PAIRS = [(a,b) for a in range(4) for b in range(a+1,4)]

class Job(Prior):
    def __init__(self, key, question, extra=()):
        self.key = self.ident = key
        self.steps, self.outputs = [], {}
        self.precision_bits = 384
        self.files = [Path(__file__), ROOT/'GEN4/duck_source_action1_20261014/programs.py', INPUT, MANIFEST,
                      BASE/'TARGET.md', BASE/'RUN_POLICY.json', *extra]
        self.binding = dict(campaign=BASE.name, profile_id=key, question=question,
            parent='H002628 completed six-clock source; chapter-I lane01 successor',
            law_namespace='SAM_land', source_heads=['H002628','H002625','H002624'],
            construction_author='Codex; installed GEN6 Duck native execution',
            epsilon_chart='I_s=hbar; t_u=t_SW/lambda_ref; epsilon=1/573049',
            preparation='Separate labelled placement reference, spectral source lanes, and coherent exact hard charge0/1 branches with common soft vacuum',
            both_helicities=True, counterrotating=True, photon_cutoff=False,
            original_completed_sources_preserved=True, coefficients_fitted=False)
    def admit(self,k,entries,p):
        return self.op(k,'GEN3_COMPLEX_ADMIT',dict(matrix=wire(entries)),p)
    def adopt(self,k,value,p):
        return self.op(k,'GEN3_COMPLEX_ADMIT',dict(matrix=deepcopy(value)),p)
    def add(self,k,n,m,terms,p):
        return self.prod(k,wire([[coef if i==j%n else 0 for name,coef in terms for j in range(n)] for i in range(n)]),
            wire([[cell(name,i,j) for j in range(m)] for name,coef in terms for i in range(n)]),p)
    def scale(self,k,x,n,c,p):
        return self.prod(k,diag([c]*n),matrix(x),p)
    def assert_zero(self,k,n,m):
        self.steps[-1 if self.steps[-1]['id']==k else next(i for i,s in enumerate(self.steps) if s['id']==k)]['checks'] += [
            dict(predicate='interval_contains',value='0',path=['result','output','matrix','entries',i,j,part])
            for i in range(n) for j in range(m) for part in ['re','im']]
    def positive(self,k,n,indices=None):
        step=next(s for s in self.steps if s['id']==k)
        for i in range(n) if indices is None else indices:
            step['checks'] += [dict(predicate='interval_positive',path=['result','output','matrix','entries',i,i,'re']),
                               dict(predicate='interval_contains',value='0',path=['result','output','matrix','entries',i,i,'im'])]
    def sqrt(self,k,x,n):
        self.admit(k+'_real',diag([dict(re={'$step':x,'path':['result','output','matrix','entries',i,i,'re']},im='0') for i in range(n)])['entries'],'Receive the proven real positive diagonal form')
        self.positive(k+'_real',n)
        # Installed GEN3_COMPLEX_LOG returns the retained -log convention.
        self.op(k+'_negative_log','GEN3_COMPLEX_LOG',dict(matrix={**diag([cell(k+'_real',i,i) for i in range(n)]),'structure':'HERMITIAN'},tolerance='1e-100',max_terms=2048),'Certified negative matrix logarithm in the installed convention')
        self.scale(k+'_half_log',k+'_negative_log',n,'-1/2','Convert retained negative-log convention to positive square-root exponent')
        self.op(k,'GEN3_COMPLEX_EXP',dict(matrix=matrix(k+'_half_log')),'Certified positive square root')
    def make_task(self,controller,target='PARENT',consumes=None):
        p=BASE/'jobs'/(self.key+'.json');save(p,self.build())
        task=dict(key=self.key,controller=controller,kind='gen6_job',job_path=str(p),job_sha256=sha(p),
                  source_binding=deepcopy(self.binding),purpose=self.binding['question'],target_id=target,
                  estimated_memory_bytes=402653184)
        if consumes is not None:task['consumes']=consumes
        return task

def scalar(j,k,value,p):j.admit(k,[[value]],p)
def clock(j,k):j.adopt(k,DATA['clock_outputs'][k],'Adopt authenticated exact completed clock operand '+k)

def lane01():
    j=Job('r1_lane01_complete_source','Receive exact source roots and construct the chapter lane01 Hamiltonian, even energy, signed currents and both counterterms; distinguish placement calibration from the clock preparation')
    j.adopt('q',DATA['q'],'Reuse certified source roots with their retained exact rational endpoints')
    j.adopt('epsilon',DATA['epsilon'],'Reuse exact capacity-normalized receiving scale')
    scalar(j,'q0',cell('q',0,0),'First certified source root')
    scalar(j,'q1',cell('q',1,1),'Second certified source root')
    j.add('d',1,1,[('q0',1),('q1',-1)],'Signed lane01 incidence q0-q1')
    j.scale('minus_d','d',1,-1,'Check the inherited signed orientation');j.positive('minus_d',1)
    j.prod('g',matrix('epsilon'),matrix('d'),'Signed source-field coupling g=epsilon*d')
    j.prod('q0q1',matrix('q0'),matrix('q1'),'Retain even source interaction energy')
    j.add('even_unscaled',1,1,[('q0',1),('q1',1),('q0q1',1)],'Full commuting lane energy')
    j.prod('even_energy',matrix('epsilon'),matrix('even_unscaled'),'Normalized complete even source energy')
    j.admit('S',[[0,1],[1,0]],'Swap in ordered spectral basis |q0 q1>,|q1 q0>')
    j.admit('D',[[cell('d'),0],[0,cell('minus_d')]],'Signed D=d sigma_z')
    j.admit('sigma_y',[[0,dict(re='0',im='-1')],[dict(re='0',im='1'),0]],'Original oriented Pauli current')
    j.prod('C',diag([cell('d')]*2),matrix('sigma_y'),'Signed C=d sigma_y')
    j.prod('D2',matrix('D'),matrix('D'),'Full plus current square')
    j.prod('C2',matrix('C'),matrix('C'),'Full cross current square')
    j.add('current_square_closure',2,2,[('D2',1),('C2',-1)],'Both polarization current-square closure');j.assert_zero('current_square_closure',2,2)
    j.prod('SD',matrix('S'),matrix('D'),'Full ordered source incidence')
    j.scale('iSD','SD',2,dict(re='0',im='1'),'Original C=i Swap D')
    j.add('C_incidence_closure',2,2,[('C',1),('iSD',-1)],'Check original signed C incidence');j.assert_zero('C_incidence_closure',2,2)
    j.admit('Hsource',[[cell('even_energy'),cell('epsilon')],[cell('epsilon'),cell('even_energy')]],'Complete lane source Hamiltonian with commuting offset retained')
    j.add('lower_energy',1,1,[('even_energy',1),('epsilon',-1)],'Complete lower source branch')
    j.add('upper_energy',1,1,[('even_energy',1),('epsilon',1)],'Complete upper source branch')
    j.admit('R',[[DATA['clock_outputs']['R']['entries'][0][0]]],'Original boundary-radius certificate')
    j.prod('g2',matrix('g'),matrix('g'),'Square of the signed coupling')
    j.scale('fourR','R',1,4,'One real polarization denominator')
    j.solve('one_counterterm',matrix('fourR'),matrix('g2'),'Pay one polarization counterterm')
    j.scale('both_counterterms','one_counterterm',1,2,'Pay both independent real-polarization counterterms')
    for k in ['q0','q1','d','g','even_unscaled','even_energy','S','D','C','D2','C2','current_square_closure','C_incidence_closure','Hsource','lower_energy','upper_energy','R','one_counterterm','both_counterterms']:j.out(k,k)
    return j

def placement():
    j=Job('r1_placement_spectral_weights','Resolve the labelled calibration state into all four source spectral weights without identifying it with a hard-clock preparation')
    j.adopt('q',DATA['q'],'Retained certified simple roots')
    j.admit('I',eye(4)['entries'],'Four admitted source components')
    j.add('x',4,4,[('q',1),('I',-756)],'Characteristic-polynomial coordinate x=q-756')
    j.prod('x2',matrix('x'),matrix('x'),'Exact spectral polynomial x squared')
    j.prod('x3',matrix('x2'),matrix('x'),'Exact spectral polynomial x cubed')
    j.add('pprime',4,4,[('x3',4),('x2',-4032),('x',-28032),('I',4300800)],'Characteristic derivative at each simple root')
    j.add('cofactor_a',4,4,[('x',1),('I',-1344)],'Placement resolvent cofactor factor')
    j.add('cofactor_b',4,4,[('x2',1),('I',-1600)],'Placement resolvent cofactor second factor')
    j.prod('cofactor',matrix('cofactor_a'),matrix('cofactor_b'),'Exact original-placement resolvent cofactor')
    j.solve('weights',matrix('pprime'),matrix('cofactor'),'Spectral projector expectation p_a=<e0|P_a|e0>')
    j.positive('weights',4)
    j.admit('pcolumn',[[cell('weights',i,i)] for i in range(4)],'All four placement spectral weights')
    j.prod('sum_weights',wire([[1]*4]),matrix('pcolumn'),'Complete placement probability')
    scalar(j,'one',1,'Exact unit source norm')
    j.add('sum_residual',1,1,[('sum_weights',1),('one',-1)],'Placement projector completeness');j.assert_zero('sum_residual',1,1)
    j.prod('pq',matrix('weights'),matrix('q'),'Complete first source moment')
    j.prod('q2',matrix('q'),matrix('q'),'Complete source square')
    j.prod('pq2',matrix('weights'),matrix('q2'),'Complete second source moment')
    for k,expected in [('pq',756),('pq2',583952)]:
        j.prod(k+'_sum',wire([[1]*4]),wire([[cell(k,i,i)] for i in range(4)]),'Retain original placement source moment')
        scalar(j,k+'_expected',expected,'Exact original-basis moment')
        j.add(k+'_residual',1,1,[(k+'_sum',1),(k+'_expected',-1)],'Check spectral reconstruction of labelled preparation');j.assert_zero(k+'_residual',1,1)
    for k in ['weights','sum_weights','sum_residual','pq_sum','pq_residual','pq2_sum','pq2_residual']:j.out(k,k)
    return j

def uniform():
    j=Job('r1_uniform_whole_cycle_clocks','Use monotonic all-time energy/amplitude envelopes to certify whole-cycle clock eligibility, preserving all six outcomes and unresolved lanes')
    for k in ['epsilon','Delta','g','mu','counterterm','Kprep','M_lower','CYCLE_E','time_CYCLE','vsoft']:clock(j,k)
    j.scale('minus_g','g',6,-1,'Retain negative signed coupling and its positive magnitude');j.positive('minus_g',6)
    for k in ['epsilon','Delta','mu','counterterm','Kprep','M_lower','CYCLE_E','time_CYCLE','vsoft']:j.positive(k,6)
    j.prod('g2',matrix('g'),matrix('g'),'Signed source coupling square')
    j.prod('alpha_raw',matrix('g2'),matrix('vsoft'),'All-order soft source coefficient')
    j.scale('alpha','alpha_raw',6,4,'Positive all-order exponent coefficient');j.positive('alpha',6)
    j.prod('source_error_T',matrix('epsilon'),matrix('CYCLE_E'),'Monotonic source-energy error at T')
    j.add('Kt_T',6,6,[('Kprep',1),('source_error_T',1)],'All-time positive field account bounded at cycle endpoint')
    j.sqrt('sqrt_c','counterterm',6);j.sqrt('sqrt_Kt','Kt_T',6)
    j.add('Ef_root_T',6,6,[('sqrt_c',1),('sqrt_Kt',1)],'Whole-field free energy bound root')
    j.prod('Ef_T',matrix('Ef_root_T'),matrix('Ef_root_T'),'Uniform full-field energy bound on [0,T]')
    j.prod('mu_Ef_T',matrix('mu'),matrix('Ef_T'),'Complete continuum energy-form payment')
    j.prod('g2_mu_Ef_T',matrix('g2'),matrix('mu_Ef_T'),'Both signed source/current correlations through the full field')
    j.sqrt('rate_root_T','g2_mu_Ef_T',6)
    j.scale('rate_numerator_T','rate_root_T',6,4,'Both quadrature contributions to actual phase-rate error')
    j.add('amplitude_min_T',6,6,[('M_lower',1),('CYCLE_E',-1)],'Uniform nonzero current-amplitude bound');j.positive('amplitude_min_T',6)
    j.solve('uniform_rate_error',matrix('amplitude_min_T'),matrix('rate_numerator_T'),'Uniform actual-rate error, using monotonic valid pointwise form bound')
    j.add('uniform_rate_lower',6,6,[('Delta',1),('uniform_rate_error',-1)],'All six uniform rate lower bounds, including unresolved signs')
    j.add('uniform_rate_upper',6,6,[('Delta',1),('uniform_rate_error',1)],'All six uniform rate upper bounds')
    for k in ['alpha','source_error_T','Kt_T','Ef_T','amplitude_min_T','uniform_rate_error','uniform_rate_lower','uniform_rate_upper']:j.out(k,k)
    j.outputs['theorem_scope']=dict(status='ANALYTIC_CONTRACT',value=dict(interval='0<=t<=T, T=time_CYCLE',hypotheses='Retained coherent exact hard branches plus common soft vacuum; all-time E/K/field-form/amplitude inequalities',method='Monotonic E(t), increasing numerator bounds and decreasing positive amplitude bound; no differentiation of accumulated phase envelope',unresolved_policy='A zero-containing lower/upper enclosure is retained; no clock inverse assigned there'))
    return j

def main():
    tasks=[];checks=[]
    for job,controller in [(lane01(),'G6_01'),(placement(),'G6_02'),(uniform(),'G6_03')]:
        task=job.make_task(controller);tasks.append(task)
        sys.path.insert(0,str(ROOT/'SAM_PROJECT/gen6_duck_t500/active_core'))
        from sam_one_principle.adapter import validate
        checks.append(dict(key=job.key,steps=len(job.steps),validation=validate(json.loads(Path(task['job_path']).read_text()))))
    save(BASE/'ops/R1_TASKS.json',tasks)
    sources={str(p):dict(path=str(p),sha256=sha(p)) for p in [INPUT,MANIFEST,Path(__file__),BASE/'TARGET.md',BASE/'RUN_POLICY.json']}
    for task in tasks:
        p=Path(task['job_path']);sources[str(p)]=dict(path=str(p),sha256=sha(p))
        for s in json.loads(p.read_text())['sources']:sources[s['path']]=s
    plan=dict(law_namespace='SAM_land',scope='Chapter I lane01 source-to-clock worked example, exact preparation map, and whole-cycle clock eligibility using retained full-continuum source results',research=dict(mode='focused'),sources=list(sources.values()),round1=tasks)
    save(BASE/'ops/PLAN.json',plan);save(BASE/'ops/COMPILER_VALIDATION.json',checks)
    print(json.dumps(dict(status='COMPILED_NO_SCIENCE',tasks=len(tasks),steps=sum(c['steps'] for c in checks),plan=str(BASE/'ops/PLAN.json'))))

if __name__=='__main__':main()
