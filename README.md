# api_camara
Scrape open data of the Brazilian Chamber of Deputies


**camara_api** class collects information on the https://dadosabertos.camara.leg.br/api/v2/
website in a more practical and faster way.

    The parameters calling the class are the current legislature (legis) and a 
    flag that indicates which block is wanting to be collected. 
    Block options are:
        - blocos
        - deputados
        - eventos
        - frentes
        - legislaturas
        - partidos
        - proposicoes
        - votacoes
        - orgaos
        - lideres

    Each block has its specific list of sub-items    

    The scrapp_data function collects data automatically. The function parameters are:
        - sub_flag: sub item of each block (eg for the deputies block, the sub_flag can be expenses, speeches, id, etc)
        - id_list: id_list is the list of information each block needs. for the legislature block, it would be a list of the desired legislatures.
        - df_legis: table with all legislatures. available at http://dadosabertos.camara.leg.br/arquivos/legislaturas/formato/legislaturas.csv
        - df_legis: table the history of all deputies. available at http://dadosabertos.camara.leg.br/arquivos/deputados/formato/deputados.csv   


**download_file** function downloads and aggregates the files available at https://dadosabertos.camara.leg.br/swagger/api.html#staticfile.

     The function parameters are:
         - flag: which file type is wanted to get. E.g proposicoes, proposicoesTemas, legislaturas, orgaos, deputados, etc.
         - year_list: if the flag above needs a year parameter in the collection, this list passes the desired years. default=None
