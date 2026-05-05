from tespy.networks import Network
from tespy.connections import Connection
from CoolProp.CoolProp import PropsSI

my_plant = Network(T_unit='K', p_unit='kPa', h_unit='kJ / kg' , s_unit='kJ / kgK')

from tespy.components import (Source, Sink, Valve, MovingBoundaryHeatExchanger, Compressor,SimpleHeatExchanger, DropletSeparator, Turbine,Splitter, Merge)
from tespy.components import PowerSource, PowerBus, PowerSink
from tespy.connections import PowerConnection
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Componentes do ciclo
fonte1 = Source("He")
fonte2 = Source("N2")
comp1 = Compressor("compressor 1")
comp2 = Compressor("compressor 2")
trc1 = SimpleHeatExchanger("resfriador 1")
trc2 = SimpleHeatExchanger("resfriador 2")
PC1 = MovingBoundaryHeatExchanger("PC1")
HEx1 = MovingBoundaryHeatExchanger("HEx1")
HEx2 = MovingBoundaryHeatExchanger("HEx2")
HEx3 = MovingBoundaryHeatExchanger("HEx3")
HEx4 = MovingBoundaryHeatExchanger("HEx4")
HEx5 = MovingBoundaryHeatExchanger("HEx5")
HEx6 = MovingBoundaryHeatExchanger("HEx6")
exp1 = Turbine("expansor 1")
exp2 = Turbine("expansor 2")
split1 = Splitter("separador vazão 1", num_out = 2)
split2 = Splitter("separador vazão 2", num_out = 2)
merge1 = Merge("merge 1", num_in = 2)
merge2 = Merge("merge 2", num_in = 2)
va = Valve("valvula JT")
sinkL = Sink("sumidouro líquido/He")
sinkG = Sink("sumidouro gás/He")
sinkN2 = Sink("sumidouro N2")
sep = DropletSeparator("separador")

#Criação da rede
c0 = Connection(fonte1, 'out1', comp1, 'in1', label='0')
c0a = Connection(comp1, 'out1', trc1, 'in1', label='0a')
c0b = Connection(trc1, 'out1', comp2, 'in1', label='0b')
c0c = Connection(comp2, 'out1', trc2, 'in1', label='0c')
c1 = Connection(trc2, 'out1', HEx1, 'in1', label='1')
c2a = Connection(HEx1, 'out1', PC1, 'in1', label='2a')
c2b = Connection(PC1, 'out1', HEx2, 'in1', label='2b')
c3 = Connection(HEx2, 'out1', split1, 'in1', label='3')
c3a = Connection(split1, 'out1', exp1, 'in1', label='3a')
c3b = Connection(split1, 'out2', HEx3, 'in1', label='3b')
c4 = Connection(HEx3, 'out1', HEx4, 'in1', label='4')
c5 = Connection(HEx4, 'out1', split2, 'in1', label='5')
c5a = Connection(split2, 'out1', exp2, 'in1', label='5a')
c5b = Connection(split2, 'out2', HEx5, 'in1', label='5b')
c6 = Connection(HEx5, 'out1', HEx6, 'in1', label='6')
c7 = Connection(HEx6, 'out1', va, 'in1', label='7')
c8 = Connection(va, 'out1', sep, 'in1', label='8')
cL = Connection(sep, 'out1', sinkL , 'in1', label='L')
cG = Connection(sep, 'out2', HEx6 , 'in2', label='G')
c9a = Connection(HEx6, 'out2', merge2, 'in1', label='9a')
c9b = Connection(exp2, 'out1', merge2, 'in2', label='9b')
c9 = Connection(merge2, 'out1', HEx5, 'in2', label='9')
c10 = Connection(HEx5, 'out2', HEx4, 'in2', label='10')
c11a = Connection(HEx4, 'out2', merge1, 'in1', label='11a')
c11b = Connection(exp1, 'out1', merge1, 'in2', label='11b')
c11 = Connection(merge1, 'out1', HEx3, 'in2', label='11')
c12 = Connection(HEx3, 'out2', HEx2, 'in2', label='12')
c13 = Connection(HEx2, 'out2', HEx1, 'in2', label='13')
c14 = Connection(HEx1, 'out2', sinkG, 'in1', label='14')

ca = Connection(fonte2, 'out1', PC1, 'in2', label='N2a')
cb = Connection(PC1, 'out2', sinkN2 , 'in1', label='N2b')

#Geração de energia eletrica
grid = PowerSource("grid")
bus = PowerBus("power bus", num_in=3, num_out=2)
ee_in = PowerConnection(grid, "power", bus, "power_in1", label="ee_in")
ee1 = PowerConnection(bus, "power_out1", comp1, "power", label="ee1")
ee2 = PowerConnection(bus, "power_out2", comp2, "power", label="ee2")
ee3 = PowerConnection(exp1, "power", bus, "power_in2", label="ee3")
ee4 = PowerConnection(exp2, "power", bus, "power_in3", label="ee4")

#Calor retirado da compressão para os dois compressores 
cooling1 = PowerSink("cooling 1") 
trc1.set_attr(power_connector_location="outlet") 
h1 = PowerConnection(trc1, "heat", cooling1, "power", label="h1") 

cooling2 = PowerSink("cooling 2") 
trc2.set_attr(power_connector_location="outlet") 
h2 = PowerConnection(trc2, "heat", cooling2, "power", label="h2")

my_plant.add_conns(c0,c0a,c0b,c0c,c1,c2a,c2b,c3,c3a,c3b,c4,c5,c5a,c5b,c6,c7,c8,cL,cG,c9,c9a,c9b,c10,c11,c11a,c11b,c12,c13,c14,ca,cb, ee_in, ee1, ee2, ee3, ee4,h1, h2)

#Parametros base
m_comp = 1 
Pmin = 100
Pmax = 1500
Pint = pow(Pmin*Pmax,0.5)
x1=0.4
x2=0.4
eta_is_exp=0.75
exp1.set_attr(eta_s = eta_is_exp) 
exp2.set_attr(eta_s = eta_is_exp)
eta_is_comp = 0.85  
comp1.set_attr(eta_s= eta_is_comp)
comp2.set_attr(eta_s= eta_is_comp)
trc1.set_attr(pr=1)    
trc2.set_attr(pr=1)          
HEx1.set_attr(pr1=1, pr2=1)
HEx2.set_attr(pr1=1, pr2=1)
HEx3.set_attr(pr1=1, pr2=1)
HEx4.set_attr(pr1=1, pr2=1)
HEx5.set_attr(pr1=1, pr2=1)
HEx6.set_attr(pr1=1, pr2=1)
PC1.set_attr(pr1=1, pr2=1)

#Inicialização com temperaturas fixas para a primeira convergência 
c0.set_attr(m=m_comp, p=Pmin, T=300, fluid={'He': 1})
c0a.set_attr(p=Pint)
c0b.set_attr(T=300)
c0c.set_attr(p=Pmax)
c1.set_attr(T=300)
c2a.set_attr(T=160)
c2b.set_attr(T=80)
c3.set_attr(T=30)
c3a.set_attr(m=x1*m_comp)
c4.set_attr(T=15)
c5.set_attr(T=10)
c5a.set_attr(m=x2*m_comp)
c6.set_attr(T=8.5)  #chute
c7.set_attr(T=7.5)
c8.set_attr(p = Pmin)
ca.set_attr(p = Pmin, x=0, fluid = {'N2':1}) 
cb.set_attr(x=1)

my_plant.solve('design')

#Depois de convergir, definimos como fixo os parametros dos trocadores 
c2a.set_attr(T=None)
c2b.set_attr(T=None)
c3.set_attr(T=None)
c4.set_attr(T=None)
c5.set_attr(T=None)
c6.set_attr(T=None)
c7.set_attr(T=None)
ef_HEx = 0.95
HEx1.set_attr(eff_max = ef_HEx)
HEx2.set_attr(eff_max = ef_HEx)
HEx3.set_attr(eff_max = ef_HEx)
HEx4.set_attr(eff_max = ef_HEx)
HEx5.set_attr(eff_max = ef_HEx)
HEx6.set_attr(eff_max = ef_HEx)
PC1.set_attr(eff_max = ef_HEx)

my_plant.solve(mode='design')
my_plant.print_results()

#Calculo da exergia
from exerpy import ExergyAnalysis
p0 = 101300
T0 = 298.15

ean = ExergyAnalysis.from_tespy(my_plant, T0, p0, split_physical_exergy=True)
fuel = {"inputs": ["ee_in","0","N2a"], "outputs": ["14","N2b"]}
#input:corrente eletrica + helio entrando no sistema + N2 entrando
#output: helio saindo do sistema + N2 saindo

product = {"inputs": ["L"], "outputs": []}
#input: helio liquido

loss = {"inputs": ["h1","h2"], "outputs": []}
#input:calor retirado da compressão

ean.analyse(E_F=fuel, E_P=product, E_L=loss)
df_components, df_material_connections, df_non_material_connections = ean.exergy_results()

#Calculo dos parametros de desempenho 
y = cL.m.val / m_comp
Wnet = (comp1.P.val + comp2.P.val + exp1.P.val + exp2.P.val) / 1e3
COP=(y * (c0.h.val-cL.h.val)) /(Wnet / m_comp)

# estado de referência em kJ/kg e kJ/kgK
h0 = PropsSI("H", "T", T0, "P", p0, "Helium") / 1000
s0 = PropsSI("S", "T", T0, "P", p0, "Helium") / 1000

#Calculo da eficiencia da coldbox
ex14 = (c14.h.val - h0) - T0 * (c14.s.val - s0)
ex1 = (c1.h.val - h0) - T0 * (c1.s.val - s0)
exL = (cL.h.val - h0) - T0 * (cL.s.val - s0)
cb = ((cL.m.val * (exL - ex14)) / (m_comp * (ex1 - ex14))) * 100

#Lista dos trocadores, será usada dentro dos loops 
hex_list = [HEx1, HEx2, HEx3, HEx4, HEx5, HEx6,PC1]


#Análise da variação da pressão máxima 
#loop dos parâmetros y, COP e eficiencia exergetica do ciclo
Pmax_values = range(350, 1940, 50)
results_pmax = []
for Pmax in Pmax_values:
    try:
        c0c.set_attr(p=Pmax)
        Pint = pow(Pmin * Pmax, 0.5)
        c0a.set_attr(p=Pint)             
        my_plant.solve(mode='design')
        
        if not my_plant.converged:
            print("Não convergiu em Pmax =", Pmax)
            results_pmax.append([Pmax, np.nan, np.nan,np.nan,np.nan, np.nan])
            continue
        
        #checagem das efetividades dos trocadores
        effs = [hx.eff_cold.val for hx in hex_list] + [hx.eff_hot.val for hx in hex_list]
        if (not np.all(np.isfinite(effs))) or (np.min(effs) < 0) or (np.max(effs) > 1):
            print(f"[ALERTA] Pmax={Pmax}: efetividade fora de [0,1] -> min={np.min(effs):.4f}, max={np.max(effs):.4f}")
            results_pmax.append([Pmax, np.nan, np.nan, np.nan,np.nan, np.nan])
            continue
        
        #checagem do pinch
        tds = [hx.td_pinch.val for hx in hex_list]
        if (not np.all(np.isfinite(tds))) or (np.min(tds) <= 0):
           print(f"[ALERTA] Pmax={Pmax}: td_pinch inválido/≤0 -> min={np.min(tds):.4f} K")
           results_pmax.append([Pmax, np.nan, np.nan, np.nan,np.nan, np.nan])
           continue
        
        y=cL.m.val/m_comp
        Wnet = (comp1.P.val + comp2.P.val + exp1.P.val + exp2.P.val) / 1e3
        OP = (y / Wnet) * 1e5
        COP=(y*(c0.h.val-cL.h.val))/(Wnet/m_comp)
        
        ean = ExergyAnalysis.from_tespy(my_plant, T0, p0, split_physical_exergy=True)
        fuel = {"inputs": ["ee_in","0","N2a"], "outputs": ["14","N2b"]}
        product = {"inputs": ["L"], "outputs": []}
        loss = {"inputs": ["h1","h2"], "outputs": []}
        ean.analyse(E_F=fuel, E_P=product, E_L=loss)
        df_components, df_material_connections, df_non_material_connections = ean.exergy_results()
        eps_tot = float(df_components.loc["TOT", "ε [%]"])
        
        ex14 = (c14.h.val - h0) - T0 * (c14.s.val - s0)
        ex1 = (c1.h.val - h0) - T0 * (c1.s.val - s0)
        exL = (cL.h.val - h0) - T0 * (cL.s.val - s0)
        eps_cb = ((cL.m.val * (exL - ex14)) / (m_comp * (ex1 - ex14))) * 100

        results_pmax.append([Pmax, y, OP, eps_tot,COP, eps_cb])

    except Exception as e:
        print("Falhou em Pmax =", Pmax, "| erro:", e)
        results_pmax.append([Pmax, np.nan, np.nan, np.nan, np.nan, np.nan])

df_pmax = pd.DataFrame(results_pmax,columns=["Pmax", "y", "y/Wnet", "ε_ciclo [%]","COP","ε_coldbox [%]"])
df_pmax.to_excel("LN2A_pmax.xlsx", index=False)

#loop para eficiencia exergetica e destruição de exergia de cada componentes
Pmax_values = range(350, 1940, 50)
results_ex_comp = []
for Pmax in Pmax_values:
    try:
        c0c.set_attr(p=Pmax)
        Pint = pow(Pmin * Pmax, 0.5)
        c0a.set_attr(p=Pint)             
        my_plant.solve(mode='design')

        if not my_plant.converged:
            print("Não convergiu em Pmax =", Pmax)
            continue

        effs = [hx.eff_cold.val for hx in hex_list] + [hx.eff_hot.val for hx in hex_list]
        if (not np.all(np.isfinite(effs))) or (np.min(effs) < 0) or (np.max(effs) > 1):
            print(f"[ALERTA] Pmax={Pmax}: efetividade fora de [0,1] -> min={np.min(effs):.4f}, max={np.max(effs):.4f}")
            continue

        tds = [hx.td_pinch.val for hx in hex_list]
        if (not np.all(np.isfinite(tds))) or (np.min(tds) <= 0):
            print(f"[ALERTA] Pmax={Pmax}: td_pinch inválido/≤0 -> min={np.min(tds):.4f} K")
            continue

        ean = ExergyAnalysis.from_tespy(my_plant, T0, p0, split_physical_exergy=True)
        fuel = {"inputs": ["ee_in","0","N2a"], "outputs": ["14","N2b"]}
        product = {"inputs": ["L"], "outputs": []}
        loss = {"inputs": ["h1","h2"], "outputs": []}
        ean.analyse(E_F=fuel, E_P=product, E_L=loss)
        df_components, df_material_connections, df_non_material_connections = ean.exergy_results()

        #lista dos componentes
        df_components = df_components.set_index("Component")
        componentes_interesse = ["compressor 1","compressor 2","expansor 1","expansor 2","HEx1","HEx2","HEx3","HEx4","HEx5","HEx6","PC1","resfriador 1","resfriador 2","valvula JT"]

        for comp in componentes_interesse:
            try:
                eps_comp = float(df_components.loc[comp, "ε [%]"])
                ED_comp = float(df_components.loc[comp, "E_D [kW]"])

                results_ex_comp.append([Pmax, comp, eps_comp, ED_comp])

            except Exception as e:
                print(f"[ALERTA] Pmax={Pmax}: falha ao ler componente {comp} | erro: {e}")
                results_ex_comp.append([Pmax, comp, np.nan, np.nan])

    except Exception as e:
        print("Falhou em Pmax =", Pmax, "| erro:", e)

df_ex_comp = pd.DataFrame(results_ex_comp,columns=["Pmax", "componente", "ε [%]", "E_D [kW]"])
df_ex_comp.to_excel("LN2A_exergia_componentes_pmax.xlsx", index=False)


#Análise da variação da eficiência dos expansores 
#loop dos parâmetros y, COP e eficiencia exergetica do ciclo
eta_values = np.arange(0.5,0.95,0.05)
results_eta =[]
for eta_is_exp in eta_values:
    try:
        exp1.set_attr(eta_s = eta_is_exp) 
        exp2.set_attr(eta_s = eta_is_exp)
        my_plant.solve(mode='design')
        
        if not my_plant.converged:
            print("Não convergiu em eficiencia =", eta_is_exp)
            results_eta.append([eta_is_exp, np.nan, np.nan,np.nan,np.nan,np.nan])
            continue
        
        effs = [hx.eff_cold.val for hx in hex_list] + [hx.eff_hot.val for hx in hex_list]
        if (not np.all(np.isfinite(effs))) or (np.min(effs) < 0) or (np.max(effs) > 1):
            results_eta.append([eta_is_exp, np.nan, np.nan,np.nan,np.nan,np.nan])
            continue
        tds = [hx.td_pinch.val for hx in hex_list]
        if (not np.all(np.isfinite(tds))) or (np.min(tds) <= 0):
           results_eta.append([eta_is_exp, np.nan, np.nan,np.nan,np.nan,np.nan])
           continue
        
        y = cL.m.val / m_comp
        Wnet = (comp1.P.val + comp2.P.val + exp1.P.val + exp2.P.val) / 1e3
        OP = (y / Wnet) * 1e5
        COP=(y*(c0.h.val-cL.h.val))/(Wnet/m_comp)
        
        ean = ExergyAnalysis.from_tespy(my_plant, T0, p0, split_physical_exergy=True)
        fuel = {"inputs": ["ee_in","0","N2a"], "outputs": ["14","N2b"]}
        product = {"inputs": ["L"], "outputs": []}
        loss = {"inputs": ["h1","h2"], "outputs": []}
        ean.analyse(E_F=fuel, E_P=product, E_L=loss)
        df_components, df_material_connections, df_non_material_connections = ean.exergy_results()
        eps_tot = float(df_components.loc["TOT", "ε [%]"])
        
        ex14 = (c14.h.val - h0) - T0 * (c14.s.val - s0)
        ex1 = (c1.h.val - h0) - T0 * (c1.s.val - s0)
        exL = (cL.h.val - h0) - T0 * (cL.s.val - s0)
        eps_cb = ((cL.m.val * (exL - ex14)) / (m_comp * (ex1 - ex14))) * 100
        
        results_eta.append([eta_is_exp, y, OP, eps_tot,COP,eps_cb])
        
    except Exception as e:
        print("Falhou em eficiencia =", eta_is_exp, "| erro:", e)
        results_eta.append([eta_is_exp, np.nan, np.nan,np.nan,np.nan,np.nan])
        
df_eta = pd.DataFrame(results_eta, columns=["eta_exp","y","y/Wnet","ε [%]","COP","ε_coldbox [%]"])
df_eta.to_excel("LN2A_eta_exp.xlsx", index=False)

#loop para eficiencia exergetica e destruição de exergia de cada componente
eta_values = np.arange(0.5,0.95,0.05)
results_ex_comp_eta = []
for eta_is_exp in eta_values:
    try:
        exp1.set_attr(eta_s=eta_is_exp)
        exp2.set_attr(eta_s=eta_is_exp)
        my_plant.solve(mode='design')

        if not my_plant.converged:
            print("Não convergiu em eficiencia =", eta_is_exp)
            continue

        effs = [hx.eff_cold.val for hx in hex_list] + [hx.eff_hot.val for hx in hex_list]
        if (not np.all(np.isfinite(effs))) or (np.min(effs) < 0) or (np.max(effs) > 1):
            print(f"[ALERTA] eficiencia={eta_is_exp}: efetividade fora de [0,1] -> min={np.min(effs):.4f}, max={np.max(effs):.4f}")
            continue

        tds = [hx.td_pinch.val for hx in hex_list]
        if (not np.all(np.isfinite(tds))) or (np.min(tds) <= 0):
            print(f"[ALERTA] eficiencia={eta_is_exp}: td_pinch inválido/≤0 -> min={np.min(tds):.4f} K")
            continue

        ean = ExergyAnalysis.from_tespy(my_plant, T0, p0, split_physical_exergy=True)
        fuel = {"inputs": ["ee_in","0","N2a"], "outputs": ["14","N2b"]}
        product = {"inputs": ["L"], "outputs": []}
        loss = {"inputs": ["h1","h2"], "outputs": []}
        ean.analyse(E_F=fuel, E_P=product, E_L=loss)
        df_components, df_material_connections, df_non_material_connections = ean.exergy_results()

        #lista dos componentes
        df_components = df_components.set_index("Component")
        componentes_interesse = ["compressor 1","compressor 2","expansor 1","expansor 2","HEx1","HEx2","HEx3","HEx4","HEx5","HEx6","PC1","resfriador 1","resfriador 2","valvula JT"]

        for comp in componentes_interesse:
            try:
                eps_comp = float(df_components.loc[comp, "ε [%]"])
                ED_comp = float(df_components.loc[comp, "E_D [kW]"])

                results_ex_comp_eta.append([eta_is_exp, comp, eps_comp, ED_comp])

            except Exception as e:
                print(f"[ALERTA] eficiencia={eta_is_exp}: falha ao ler componente {comp} | erro: {e}")
                results_ex_comp_eta.append([eta_is_exp, comp, np.nan, np.nan])

    except Exception as e:
        print("Falhou em eficiencia =", eta_is_exp, "| erro:", e)

df_ex_comp_eta = pd.DataFrame(results_ex_comp_eta,columns=["eta_exp", "componente", "ε [%]", "E_D [kW]"])
df_ex_comp_eta.to_excel("LN2A_exergia_componentes_eta_exp.xlsx", index=False)


#Análise da variação da efetividade dos trocadores 
#loop dos parâmetros y, COP e eficiencia exergetica do ciclo
eff_values = np.arange(0.75,1.0,0.01)
results_ef =[]
for ef_HEx in eff_values:
    try:
        HEx1.set_attr(eff_max = ef_HEx)
        HEx2.set_attr(eff_max = ef_HEx)
        HEx3.set_attr(eff_max = ef_HEx)
        HEx4.set_attr(eff_max = ef_HEx)
        HEx5.set_attr(eff_max = ef_HEx)
        HEx6.set_attr(eff_max = ef_HEx)
        PC1.set_attr(eff_max = ef_HEx)
        my_plant.solve(mode='design')
        
        if not my_plant.converged:
            print("Não convergiu em efetividade =", ef_HEx)
            results_ef.append([ef_HEx, np.nan, np.nan, np.nan,np.nan,np.nan])
            continue
        
        effs = [hx.eff_cold.val for hx in hex_list] + [hx.eff_hot.val for hx in hex_list]
        if (not np.all(np.isfinite(effs))) or (np.min(effs) < 0) or (np.max(effs) > 1):
            results_ef.append([ef_HEx, np.nan, np.nan,np.nan,np.nan,np.nan])
            continue
        tds = [hx.td_pinch.val for hx in hex_list]
        if (not np.all(np.isfinite(tds))) or (np.min(tds) <= 0):
           results_ef.append([ef_HEx, np.nan, np.nan,np.nan,np.nan,np.nan])
           continue
        
        y = cL.m.val / m_comp
        Wnet = (comp1.P.val + comp2.P.val + exp1.P.val + exp2.P.val) / 1e3
        OP = (y / Wnet) * 1e5
        COP=(y*(c0.h.val-cL.h.val))/(Wnet/m_comp)
        
        ean = ExergyAnalysis.from_tespy(my_plant, T0, p0, split_physical_exergy=True)
        fuel = {"inputs": ["ee_in","0","N2a"], "outputs": ["14","N2b"]}
        product = {"inputs": ["L"], "outputs": []}
        loss = {"inputs": ["h1","h2"], "outputs": []}
        ean.analyse(E_F=fuel, E_P=product, E_L=loss)
        df_components, df_material_connections, df_non_material_connections = ean.exergy_results()
        eps_tot = float(df_components.loc["TOT", "ε [%]"])
        
        ex14 = (c14.h.val - h0) - T0 * (c14.s.val - s0)
        ex1 = (c1.h.val - h0) - T0 * (c1.s.val - s0)
        exL = (cL.h.val - h0) - T0 * (cL.s.val - s0)
        eps_cb = ((cL.m.val * (exL - ex14)) / (m_comp * (ex1 - ex14))) * 100

        results_ef.append([ef_HEx, y, OP, eps_tot,COP, eps_cb])
        
    except Exception as e:
        print("Falhou em efetividade =", ef_HEx, "| erro:", e)
        results_ef.append([ef_HEx, np.nan, np.nan,np.nan,np.nan,np.nan])       
        
df_eff = pd.DataFrame(results_ef, columns=["ef_HEx","y","y/Wnet","ε [%]","COP","ε_coldbox [%]"])
df_eff.to_excel("LN2A_eff.xlsx", index=False)

#loop para eficiencia exergetica e destruição de exergia de cada componente
eff_values = np.arange(0.75,1.0,0.01)
results_ex_comp_ef = []
for ef_HEx in eff_values:
    try:
        HEx1.set_attr(eff_max=ef_HEx)
        HEx2.set_attr(eff_max=ef_HEx)
        HEx3.set_attr(eff_max=ef_HEx)
        HEx4.set_attr(eff_max=ef_HEx)
        HEx5.set_attr(eff_max=ef_HEx)
        HEx6.set_attr(eff_max=ef_HEx)
        PC1.set_attr(eff_max=ef_HEx)
        my_plant.solve(mode='design')

        if not my_plant.converged:
            print("Não convergiu em efetividade =", ef_HEx)
            continue

        effs = [hx.eff_cold.val for hx in hex_list] + [hx.eff_hot.val for hx in hex_list]
        if (not np.all(np.isfinite(effs))) or (np.min(effs) < 0) or (np.max(effs) > 1):
            print(f"[ALERTA] efetividade={ef_HEx}: efetividade fora de [0,1] -> min={np.min(effs):.4f}, max={np.max(effs):.4f}")
            continue

        tds = [hx.td_pinch.val for hx in hex_list]
        if (not np.all(np.isfinite(tds))) or (np.min(tds) <= 0):
            print(f"[ALERTA] efetividade={ef_HEx}: td_pinch inválido/≤0 -> min={np.min(tds):.4f} K")
            continue

        ean = ExergyAnalysis.from_tespy(my_plant, T0, p0, split_physical_exergy=True)
        fuel = {"inputs": ["ee_in","0","N2a"], "outputs": ["14","N2b"]}
        product = {"inputs": ["L"], "outputs": []}
        loss = {"inputs": ["h1","h2"], "outputs": []}
        ean.analyse(E_F=fuel, E_P=product, E_L=loss)
        df_components, df_material_connections, df_non_material_connections = ean.exergy_results()

        df_components = df_components.set_index("Component")
        componentes_interesse = ["compressor 1","compressor 2","expansor 1","expansor 2","HEx1","HEx2","HEx3","HEx4","HEx5","HEx6","PC1","resfriador 1","resfriador 2","valvula JT"]

        for comp in componentes_interesse:
            try:
                eps_comp = float(df_components.loc[comp, "ε [%]"])
                ED_comp = float(df_components.loc[comp, "E_D [kW]"])

                results_ex_comp_ef.append([ef_HEx, comp, eps_comp, ED_comp])

            except Exception as e:
                print(f"[ALERTA] efetividade={ef_HEx}: falha ao ler componente {comp} | erro: {e}")
                results_ex_comp_ef.append([ef_HEx, comp, np.nan, np.nan])

    except Exception as e:
        print("Falhou em efetividade =", ef_HEx, "| erro:", e)

df_ex_comp_ef = pd.DataFrame(results_ex_comp_ef,columns=["ef_HEx", "componente", "ε [%]", "E_D [kW]"])
df_ex_comp_ef.to_excel("LN2A_exergia_componentes_efetividade.xlsx", index=False)


#Análise da variação da razão de pressão nos trocadores 
#loop dos parâmetros y, COP e eficiencia exergetica do ciclo
pres_values = np.arange(0.92,1.01,0.01)
results_pres =[]
for pr in pres_values:
    try:
        HEx1.set_attr(pr1=pr, pr2=pr)
        HEx2.set_attr(pr1=pr, pr2=pr)
        HEx3.set_attr(pr1=pr, pr2=pr)
        HEx4.set_attr(pr1=pr, pr2=pr)
        HEx5.set_attr(pr1=pr, pr2=pr)
        HEx6.set_attr(pr1=pr, pr2=pr)
        PC1.set_attr(pr1=pr, pr2=pr)
        my_plant.solve(mode='design')
        
        if not my_plant.converged:
            print("Não convergiu em perda de pressão =", pr)
            results_pres.append([pr, np.nan, np.nan, np.nan,np.nan,np.nan])
            continue
        
        effs = [hx.eff_cold.val for hx in hex_list] + [hx.eff_hot.val for hx in hex_list]
        if (not np.all(np.isfinite(effs))) or (np.min(effs) < 0) or (np.max(effs) > 1):
            results_pres.append([pr, np.nan, np.nan,np.nan,np.nan,np.nan])
            continue
        tds = [hx.td_pinch.val for hx in hex_list]
        if (not np.all(np.isfinite(tds))) or (np.min(tds) <= 0):
           results_pres.append([pr, np.nan, np.nan,np.nan,np.nan,np.nan])
           continue
        
        y = cL.m.val / m_comp
        Wnet = (comp1.P.val + comp2.P.val + exp1.P.val + exp2.P.val) / 1e3
        OP = (y / Wnet) * 1e5
        COP=(y*(c0.h.val-cL.h.val))/(Wnet/m_comp)
        
        ean = ExergyAnalysis.from_tespy(my_plant, T0, p0, split_physical_exergy=True)
        fuel = {"inputs": ["ee_in","0","N2a"], "outputs": ["14","N2b"]}
        product = {"inputs": ["L"], "outputs": []}
        loss = {"inputs": ["h1","h2"], "outputs": []}
        ean.analyse(E_F=fuel, E_P=product, E_L=loss)
        df_components, df_material_connections, df_non_material_connections = ean.exergy_results()
        eps_tot = float(df_components.loc["TOT", "ε [%]"])
        
        eps_tot = float(df_components.loc["TOT", "ε [%]"])
        ex14 = (c14.h.val - h0) - T0 * (c14.s.val - s0)
        ex1 = (c1.h.val - h0) - T0 * (c1.s.val - s0)
        exL = (cL.h.val - h0) - T0 * (cL.s.val - s0)
        eps_cb = ((cL.m.val * (exL - ex14)) / (m_comp * (ex1 - ex14))) * 100
        
        results_pres.append([pr, y, OP, eps_tot,COP,eps_cb])
        
    except Exception as e:
        print("Falhou em perda de pressão =", pr, "| erro:", e)
        results_pres.append([pr, np.nan, np.nan,np.nan,np.nan,np.nan])       
        
df_eff = pd.DataFrame(results_pres, columns=["presure ratio","y","y/Wnet","ε [%]","COP","ε_coldbox [%]"])
df_eff.to_excel("LN2A_pr.xlsx", index=False)

#loop para eficiencia exergetica e destruição de exergia de cada componente
pres_values = np.arange(0.92,1.01,0.01)
results_ex_comp_pr = []

for pr in pres_values:
    try:
        HEx1.set_attr(pr1=pr, pr2=pr)
        HEx2.set_attr(pr1=pr, pr2=pr)
        HEx3.set_attr(pr1=pr, pr2=pr)
        HEx4.set_attr(pr1=pr, pr2=pr)
        HEx5.set_attr(pr1=pr, pr2=pr)
        HEx6.set_attr(pr1=pr, pr2=pr)
        PC1.set_attr(pr1=pr, pr2=pr)
        my_plant.solve(mode='design')
        
        if not my_plant.converged:
            print("Não convergiu em razão de perda de pressão =", pr)
            continue

        effs = [hx.eff_cold.val for hx in hex_list] + [hx.eff_hot.val for hx in hex_list]
        if (not np.all(np.isfinite(effs))) or (np.min(effs) < 0) or (np.max(effs) > 1):
            print(f"[ALERTA] pr={pr}: efetividade fora de [0,1] -> min={np.min(effs):.4f}, max={np.max(effs):.4f}")
            continue

        tds = [hx.td_pinch.val for hx in hex_list]
        if (not np.all(np.isfinite(tds))) or (np.min(tds) <= 0):
            print(f"[ALERTA] pr={pr}: td_pinch inválido/≤0 -> min={np.min(tds):.4f} K")
            continue

        ean = ExergyAnalysis.from_tespy(my_plant, T0, p0, split_physical_exergy=True)
        fuel = {"inputs": ["ee_in","0","N2a"], "outputs": ["14","N2b"]}
        product = {"inputs": ["L"], "outputs": []}
        loss = {"inputs": ["h1","h2"], "outputs": []}
        ean.analyse(E_F=fuel, E_P=product, E_L=loss)
        df_components, df_material_connections, df_non_material_connections = ean.exergy_results()

        df_components = df_components.set_index("Component")
        componentes_interesse = ["compressor 1","compressor 2","expansor 1","expansor 2","HEx1","HEx2","HEx3","HEx4","HEx5","HEx6","PC1","resfriador 1","resfriador 2","valvula JT"]

        for comp in componentes_interesse:
            try:
                eps_comp = float(df_components.loc[comp, "ε [%]"])
                ED_comp = float(df_components.loc[comp, "E_D [kW]"])

                results_ex_comp_pr.append([pr, comp, eps_comp, ED_comp])

            except Exception as e:
                print(f"[ALERTA] pr={pr}: falha ao ler componente {comp} | erro: {e}")
                results_ex_comp_pr.append([pr, comp, np.nan, np.nan])

    except Exception as e:
        print("Falhou em razão de perda de pressão =", pr, "| erro:", e)

df_ex_comp_pr = pd.DataFrame(results_ex_comp_pr,columns=["pr", "componente", "ε [%]", "E_D [kW]"])
df_ex_comp_pr.to_excel("LN2A_exergia_componentes_pr.xlsx", index=False)


#Análise da variação dos parametros x1 e x2,sendo que x2 é fixo e x1 é variado num intervalo determinado
results = []
x2_values = [0.55]
x1_values = np.arange(0.1, 0.33, 0.01)

#combinações de x1 e x2 que porduzem valores positivos
#x2=0.15 -> x1 0.15-0.52  
#x2=0.2  -> x1 0.25-0.55
#x2=0.25 -> x1 0.25-0.59  
#x2=0.3  -> x1 0.2-0.54
#x2=0.35 -> x1 0.2-0.49  
#x2=0.4  -> x1 0.2-0.45
#x2=0.45 -> x1 0.15-0.41 
#x2=0.5  -> x1 0.1 -0.36
#x2=0.55 -> x1 0.1 -0.32  
#x2=0.6  -> x1 0.1 -0.26   
#x2=0.65 -> x1 0.1 -0.22
for x2 in x2_values:
    for x1 in x1_values:
        if x1 + x2 >= 1:
            continue
        try:
            c3a.set_attr(m=x1 * m_comp)
            c5a.set_attr(m=x2 * m_comp)
            my_plant.solve(mode='design')
 
            effs = [hx.eff_cold.val for hx in hex_list] + [hx.eff_hot.val for hx in hex_list]
            if (not np.all(np.isfinite(effs))) or (np.min(effs) < 0) or (np.max(effs) > 1):
                results.append([Pmax, np.nan, np.nan, np.nan])
                continue
            tds = [hx.td_pinch.val for hx in hex_list]
            if (not np.all(np.isfinite(tds))) or (np.min(tds) <= 0):
               results.append([Pmax, np.nan, np.nan, np.nan])
               continue

            y = cL.m.val / m_comp
            Wnet = (comp1.P.val + comp2.P.val + exp1.P.val + exp2.P.val) / 1e3
            OP = (y / Wnet) * 1e5
            ean = ExergyAnalysis.from_tespy(my_plant, T0, p0, split_physical_exergy=True)
            fuel = {"inputs": ["ee_in","0","N2a"], "outputs": ["14","N2b"]}
            product = {"inputs": ["L"], "outputs": []}
            loss = {"inputs": ["h1","h2"], "outputs": []}
            ean.analyse(E_F=fuel, E_P=product, E_L=loss)
            df_components, df_material_connections, df_non_material_connections = ean.exergy_results()
            eps_tot = float(df_components.loc["TOT", "ε [%]"])
            results.append([x1, x2, y, OP, eps_tot])
        
        except Exception as e:
            print(f"Falhou em x1={x1:.2f}, x2={x2:.2f} | erro: {e}")
            results.append([x1, x2, np.nan, np.nan, np.nan])

df_x1 = pd.DataFrame(results, columns=["x1", "x2", "y","y/Wnet" ,"ε [%]"])
df_x1.to_excel("LN2A_x2=0.55.xlsx", index=False)
