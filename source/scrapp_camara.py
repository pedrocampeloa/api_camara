# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 00:33:27 2023
@author: Pedro
"""

import pandas as pd
import json
import os
import datetime as dt
import requests
import time


class camara_api:
    
    """
    This function collects information on the https://dadosabertos.camara.leg.br/api/v2/
    website in a more practical and faster way.
    
    The parameters calling the class are the current legislature (legis) and a 
    flag that indicates which block is wanting to be collected. 
    Block options are ['blocos','deputados','eventos','frentes', 'legislaturas','partidos','proposicoes','votacoes','orgaos','lideres']
    
    Each block has its specific list of sub-items        
    The scrapp_data function collects data automatically. The function parameters are:
    
        - sub_flag: sub item of each block (eg for the deputies block, the sub_flag can be expenses, speeches, id, etc)
        - id_list: id_list is the list of information each block needs. for the legislature block, it would be a list of the desired legislatures.
        - df_legis: table with all legislatures. available at http://dadosabertos.camara.leg.br/arquivos/legislaturas/formato/legislaturas.csv
        - df_legis: table the history of all deputies. available at http://dadosabertos.camara.leg.br/arquivos/deputados/formato/deputados.csv    
        
    """
    
    
    def __init__(self, flag, legis):
        self.legis = legis
        self.flag = flag
        self.url_ = f'https://dadosabertos.camara.leg.br/api/v2/{flag}'   
        
    def gen_url(self, sub_flag, params):
        
        id_ = params['id_']
        page = params['page']
        data_inicio = params['data_inicio']
        data_fim= params['data_fim']
                
        if self.flag == 'legislaturas':
            if sub_flag in ['id']:
                return f"{self.url_}/{id_}"  
            elif sub_flag in ['lideres']:
                complemento1='?pagina='
                complemento2='&itens=100'      
                return f"{self.url_}/{id_}/{sub_flag}{complemento1}{page}{complemento2}"            
            elif sub_flag in ['mesa']:
                complemento1='?dataInicio='
                complemento2='&dataFim='
                return f"{self.url_}/{id_}/{sub_flag}{complemento1}{data_inicio}{complemento2}{data_fim}"
            else:
                complemento1='?id='
                complemento2='&pagina='
                complemento3='&itens=100'
                return f"{self.url_}{complemento1}{id_}{complemento2}{page}{complemento3}"    

        elif self.flag == 'deputados':
            if sub_flag in ['id']:
                return f"{self.url_}/{id_}"  
            elif sub_flag in [ 'frentes', 'ocupacoes', 'profissoes', 'codSituacao', 'situacoesDeputado']:
                return  f"{self.url_}/{id_}/{sub_flag}"  
            elif sub_flag in ['discursos', 'eventos', 'orgaos']:
                complemento1='?dataInicio='
                complemento2='&dataFim='
                complemento3='&pagina='
                complemento4='&itens=100'
                return f"{self.url_}/{id_}/{sub_flag}{complemento1}{data_inicio}{complemento2}{data_fim}{complemento3}{page}{complemento4}"            
            elif sub_flag in ['lideres']:
                complemento1='?pagina='
                complemento2='&itens=100'      
                return f"{self.url_}/{id_}/{sub_flag}{complemento1}{page}{complemento2}"            
            elif sub_flag in ['mesa']:
                complemento1='?dataInicio='
                complemento2='&dataFim='
                return f"{self.url_}/{id_}/{sub_flag}{complemento1}{data_inicio}{complemento2}{data_fim}"
            elif sub_flag in [None, 'despesas']:
                complemento1='?idLegislatura='
                complemento2='&pagina='
                complemento3='&itens=100'
                return f"{self.url_}{complemento1}{id_}{complemento2}{page}{complemento3}"     
            
        elif self.flag == 'frentes':
            if sub_flag == 'id':
                return f"{self.url_}/{id_}"
            elif sub_flag == 'membros':
                return f"{self.url_}/{id_}/{sub_flag}"
            else:
                complemento1='?idLegislatura='
                complemento2='&pagina='
                complemento3='&itens=100'
                return f"{self.url_}{complemento1}{id_}{complemento2}{page}{complemento3}"
    
        elif self.flag == 'blocos':
            if sub_flag == 'id':
                return f"{self.url_}/{id_}"
            else:
                complemento1='?idLegislatura='
                complemento2='&pagina='
                complemento3='&itens=100'                
                return f"{self.url_}{complemento1}{id_}{complemento2}{page}{complemento3}"
            
        elif self.flag == 'partidos':
            if sub_flag in ['id']:
                return f"{self.url_}/{id_}"  
            elif sub_flag in ['membros']:
                complemento1='?dataInicio='
                complemento2='&dataFim='
                complemento3='&pagina='
                complemento4='&itens=100'
                return f"{self.url_}/{id_}/{sub_flag}{complemento1}{data_inicio}{complemento2}{data_fim}"#"{complemento3}{page}{complemento4}"            
            elif sub_flag in ['lideres']:
                complemento1='?pagina='
                complemento2='&itens=100'      
                return f"{self.url_}/{id_}/{sub_flag}{complemento1}{page}{complemento2}"            
            elif sub_flag in [None]:
                complemento1='?idLegislatura='
                complemento2='&pagina='
                complemento3='&itens=100'
                return f"{self.url_}{complemento1}{id_}{complemento2}{page}{complemento3}"   
        
        elif self.flag == 'orgaos':
            if sub_flag in [None]:
                complemento1='?dataInicio='
                complemento2='&dataFim='
                complemento3='&pagina='
                complemento4='&itens=100'
                return f"{self.url_}{complemento1}{data_inicio}{complemento2}{data_fim}{complemento3}{page}{complemento4}"   
            if sub_flag == 'id':
                return f"{self.url_}/{id_}"  
            if sub_flag in ['eventos', 'membros', 'votacoes']:
                complemento1='?dataInicio='
                complemento2='&dataFim='
                complemento3='&pagina='
                complemento4='&itens=100'
                return f"{self.url_}/{id_}/{sub_flag}{complemento1}{data_inicio}{complemento2}{data_fim}{complemento3}{page}{complemento4}"   
            elif sub_flag == 'situacoesOrgao':
                url_aux = 'https://dadosabertos.camara.leg.br/api/v2/referencias/'
                return f"{url_aux}/{sub_flag}"
            elif sub_flag == 'codSituacao':
                url_aux = 'https://dadosabertos.camara.leg.br/api/v2/referencias/'
                return f"{url_aux}/{self.flag}/{sub_flag}"
            
        elif self.flag == 'votacoes':
            if sub_flag in ['id']:
                return f"{self.url_}/{id_}"
            elif sub_flag in ['orientacoes', 'votos']:
                return f"{self.url_}/{id_}/{sub_flag}"
            else:
                complemento1='?dataInicio='
                complemento2='&dataFim='
                complemento3='&pagina='
                complemento4='&itens=100'
                
                data_inicio = id_[0]
                data_fim = id_[1]                
                return f"{self.url_}{complemento1}{data_inicio}{complemento2}{data_fim}{complemento3}{page}{complemento4}"   

        elif self.flag == 'proposicoes':
            if sub_flag in ['id']:
                return f"{self.url_}/{id_}"
            elif sub_flag in ['orientacoes', 'votos']:
                return f"{self.url_}/{id_}/{sub_flag}"
            else:
                complemento0='?ano='
                complemento1='&dataInicio='
                complemento2='&dataFim='
                complemento3='&pagina='
                complemento4='&itens=100'
                
                data_inicio = id_[0]
                data_fim = id_[1]
                ano = data_inicio.split('-')[0]                
                return f"{self.url_}{complemento0}{ano}{complemento1}{data_inicio}{complemento2}{data_fim}{complemento3}{page}{complemento4}"   

        elif self.flag == 'lideres':
            url_aux = 'https://dadosabertos.camara.leg.br/api/v2/'
            complemento1='&pagina='
            complemento2='&itens=100'
            return f"{url_aux}/{sub_flag}/{id_}/{self.flag}{complemento1}{page}{complemento2}"
        
        elif self.flag == 'referencias':
            return f"{self.url_}/{sub_flag}"
        
        elif self.flag == 'proposicoes':
            if sub_flag == None:

                ano = data_inicio.split('-')[0]                
                complemento0='?ano='
                complemento1='&dataInicio='
                complemento2='&dataFim='
                complemento3='&pagina='
                complemento4='&itens=100'
                return f"{self.url_}{complemento0}{ano}{complemento1}{data_inicio}{complemento2}{data_fim}{complemento3}{page}{complemento4}"   
            elif sub_flag in ['tramitacoes']:
                complemento1='?dataInicio='
                complemento2='&dataFim='
                return f"{self.url_}/{id_}/{sub_flag}{complemento1}{data_inicio}{complemento2}{data_fim}"
            else:
                return f"{self.url_}/{id_}/{sub_flag}"
                
    def get_response(self,url):
        
        response = requests.get(url, headers={"accept": "application/json"})
        item = json.loads(response.text)
        if type(item) == dict:            
            if 'dados' in item.keys():
                data = item['dados']
            else:
                data = []
        else:
            data = []
        
        return data

    def scrapp_data(self,sub_flag, id_list, df_legis = None, df_dep = None):

        full_name = f'{self.flag}_{sub_flag}'            

        data_scrapped = {}
        legis_list = [l for l in range(1,self.legis+1)]        
        
        for i,id_ in enumerate(id_list):                           
            
            if self.flag == 'deputados':                    
                legis_list = df_dep[df_dep['id']== id_]['idLegislatura'].unique()
                
                data_inicio = df_legis[df_legis['id'].isin(legis_list)]['dataInicio'].min()
                data_fim =  df_legis[df_legis['id'].isin(legis_list)]['dataFim'].max()
            elif full_name =='legislaturas_mesa':
                data_inicio = df_legis[df_legis['id'] == id_]['dataInicio'].min()
                data_fim = df_legis[df_legis['id'] == id_]['dataFim'].max()
                
            elif self.flag in ['partidos', 'orgaos']:
                data_inicio = df_legis['dataInicio'].min()
                data_fim = df_legis['dataFim'].max()

            else:
                data_inicio = ''
                data_fim = ''
            
                        
            if len(id_list)<50:
                n_prints = 5
            if len(id_list)<100 & len(id_list)>50:
                n_prints = 10
            elif len(id_list)>100 & len(id_list)<1000:
                n_prints = 100
                
            if i%n_prints==0:    
                print(f"scraping info {self.flag}-{sub_flag} from: {id_} {(i+1)}/{(len(id_list))}")
            
            page=1
            params = {'id_':id_,'page':page, 'data_inicio':data_inicio, 'data_fim':data_fim}
            url = self.gen_url(sub_flag, params)
            # print('###',url)
            try:
                json_data = self.get_response(url)                
                json_data_agg = json_data
            except:                
                try:
                    time.sleep(2)
                    json_data = self.get_response(url)                
                    json_data_agg = json_data
                except:
                    print(f"internal error {url}")
                    json_data = [{f'error_{id_}':f"internal error: {url}"}]       
            
            if 'pagina' in url:
                while(len(json_data)>0):
                    page+=1
                    if page%10 == 0:                        
                        print(f' - scrapping page {page}... - {id_} {(i+1)}/{(len(id_list))}')
                    # print(page)
                    params = {'id_':id_,'page':page, 'data_inicio':data_inicio, 'data_fim':data_fim}
                    url = self.gen_url(sub_flag, params)
                    # print(url)
                    # json_data = self.get_response(url)                
                    # json_data_agg = json_data_agg + json_data
                    
                    try:
                        json_data = self.get_response(url)                
                        json_data_agg = json_data_agg + json_data
                    except:
                        try:
                            time.sleep(2)
                            json_data = self.get_response(url)                
                            json_data_agg = json_data_agg + json_data
                        except:
                            
                            print(f"internal error {url}")
                            json_data = [{f'error_{id_}':f"internal error: {url}"}]
            
            data_scrapped[id_] = json_data_agg
        
        return data_scrapped            
  


def download_file(flag,year_list=None):
    
    """
    This function downloads and aggregates the files available at https://dadosabertos.camara.leg.br/swagger/api.html#staticfile.
    
     The function parameters are:
         - flag: which file type is wanted to get. E.g proposicoes, proposicoesTemas, legislaturas, orgaos, deputados, etc.
         - year_list: if the flag above needs a year parameter in the collection, this list passes the desired years. default=None
    """
   
    formato = 'csv'    
    df_list = []
    if year_list:
        for year in year_list:
            if year%10==0:
                print(year)
            url = f'http://dadosabertos.camara.leg.br/arquivos/{flag}/{formato}/{flag}-{year}.{formato}' 
            try:
                data = pd.read_csv(url, encoding = 'utf-8', sep = ';')
            except:
                if year%10==0:                
                    print(f" - No data for year {year}")
                data = pd.DataFrame()
            data['y'] = str(year)
            df_list.append(data)
        df = pd.concat(df_list).drop_duplicates().dropna(how='all').dropna(how='all', axis=1)

    else:
        if 'orgaosDeputados' in flag:
            flag_ = flag.split('-')[0]
            url = f"http://dadosabertos.camara.leg.br/arquivos/{flag_}/{formato}/{flag}.{formato} "       
        else:
            url = f"http://dadosabertos.camara.leg.br/arquivos/{flag}/{formato}/{flag}.{formato} "       
        df = pd.read_csv(url, encoding = 'utf-8', sep = ';')
 
    return df
    
