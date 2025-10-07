import pandas as pd
from typing import Tuple, Dict, List
import json
import csv

class CSVComparator:
    def __init__(self, key_column: str = None):
        """
        Inicializa o comparador de CSV.
        
        Args:
            key_column: Nome da coluna que será usada como chave primária.
                       Se None, será usada a primeira coluna.
        """
        self.key_column = key_column
    
    def detect_delimiter(self, file_path: str) -> str:
        """
        Detecta automaticamente o delimitador do arquivo CSV.
        
        Args:
            file_path: Caminho para o arquivo CSV
            
        Returns:
            String com o delimitador detectado
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            # Lê as primeiras linhas para detectar o delimitador
            sample = file.read(1024)
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter
            return delimiter
    
    def compare_csvs(self, file1_path: str, file2_path: str) -> Dict:
        """
        Compara dois arquivos CSV e retorna as diferenças.
        
        Args:
            file1_path: Caminho para o primeiro arquivo CSV
            file2_path: Caminho para o segundo arquivo CSV
            
        Returns:
            Dicionário com as diferenças encontradas
        """
        try:
            # NOVA FUNCIONALIDADE: Detecta delimitador automaticamente
            delimiter1 = self.detect_delimiter(file1_path)
            delimiter2 = self.detect_delimiter(file2_path)
            
            # Lê os arquivos CSV com o delimitador correto
            df1 = pd.read_csv(file1_path, sep=delimiter1)
            df2 = pd.read_csv(file2_path, sep=delimiter2)
            
            # Remove espaços em branco dos nomes das colunas
            df1.columns = df1.columns.str.strip()
            df2.columns = df2.columns.str.strip()
            
            # Define a coluna chave
            key_col = self.key_column or df1.columns[0]
            
            if key_col not in df1.columns or key_col not in df2.columns:
                raise ValueError(f"Coluna chave '{key_col}' não encontrada em um dos arquivos")
            
            # CORREÇÃO: Remove linhas com valores nulos ou vazios na coluna chave
            df1 = df1.dropna(subset=[key_col])
            df2 = df2.dropna(subset=[key_col])
            
            # CORREÇÃO: Remove espaços da coluna chave e converte para string
            df1[key_col] = df1[key_col].astype(str).str.strip()
            df2[key_col] = df2[key_col].astype(str).str.strip()
            
            # CORREÇÃO: Remove linhas vazias na coluna chave (após limpeza)
            df1 = df1[df1[key_col] != '']
            df2 = df2[df2[key_col] != '']
            
            # CORREÇÃO: Verifica se há duplicatas na coluna chave
            duplicates1 = df1[df1.duplicated(subset=[key_col], keep=False)][key_col].unique()
            duplicates2 = df2[df2.duplicated(subset=[key_col], keep=False)][key_col].unique()
            
            if len(duplicates1) > 0 or len(duplicates2) > 0:
                error_msg = "Valores duplicados encontrados na coluna chave:\n"
                if len(duplicates1) > 0:
                    error_msg += f"Arquivo 1: {list(duplicates1)}\n"
                if len(duplicates2) > 0:
                    error_msg += f"Arquivo 2: {list(duplicates2)}\n"
                error_msg += "Por favor, certifique-se de que a coluna chave tenha valores únicos."
                raise ValueError(error_msg)
            
            # NOVA FUNCIONALIDADE: Detecta diferenças nas colunas
            cols1 = set(df1.columns)
            cols2 = set(df2.columns)
            
            columns_added = list(cols2 - cols1)      # Colunas que só existem no arquivo 2
            columns_removed = list(cols1 - cols2)    # Colunas que só existem no arquivo 1
            
            # NOVA FUNCIONALIDADE: Alinha os DataFrames para ter as mesmas colunas
            all_columns = cols1.union(cols2)  # Todas as colunas dos dois arquivos
            df1_aligned = df1.reindex(columns=all_columns)  # Adiciona colunas faltantes com NaN
            df2_aligned = df2.reindex(columns=all_columns)  # Adiciona colunas faltantes com NaN
            
            # CORREÇÃO: Agora pode converter para dict sem problemas (chaves únicas)
            dict1 = df1_aligned.set_index(key_col).to_dict('index')
            dict2 = df2_aligned.set_index(key_col).to_dict('index')
            
            # Identifica as diferenças nas linhas (lógica original mantida)
            keys1 = set(dict1.keys())
            keys2 = set(dict2.keys())
            
            # Linhas novas (existem no arquivo 2, mas não no 1)
            new_keys = keys2 - keys1
            new_rows = [{'key': key, 'data': dict2[key]} for key in new_keys]
            
            # Linhas removidas (existem no arquivo 1, mas não no 2)
            removed_keys = keys1 - keys2
            removed_rows = [{'key': key, 'data': dict1[key]} for key in removed_keys]
            
            # Linhas alteradas (existem em ambos, mas com conteúdo diferente)
            common_keys = keys1 & keys2
            modified_rows = []
            
            for key in common_keys:
                if dict1[key] != dict2[key]:
                    modified_rows.append({
                        'key': key,
                        'old_data': dict1[key],
                        'new_data': dict2[key]
                    })
            
            # Prepara o resultado (agora com informações de colunas)
            result = {
                'summary': {
                    'total_rows_file1': len(df1),
                    'total_rows_file2': len(df2),
                    'new_rows': len(new_rows),
                    'removed_rows': len(removed_rows),
                    'modified_rows': len(modified_rows),
                    'unchanged_rows': len(common_keys) - len(modified_rows),
                    # NOVA FUNCIONALIDADE: Contadores de colunas
                    'columns_added': len(columns_added),
                    'columns_removed': len(columns_removed)
                },
                'new_rows': new_rows,
                'removed_rows': removed_rows,
                'modified_rows': modified_rows,
                'key_column': key_col,
                # NOVA FUNCIONALIDADE: Listas de colunas alteradas
                'columns_added': columns_added,
                'columns_removed': columns_removed
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"Erro ao comparar arquivos CSV: {str(e)}")
    
    def format_results_for_display(self, comparison_result: Dict) -> Dict:
        """
        Formata os resultados da comparação para exibição na web.
        
        Args:
            comparison_result: Resultado da comparação
            
        Returns:
            Dicionário formatado para exibição
        """
        formatted = {
            'summary': comparison_result['summary'],
            'key_column': comparison_result['key_column'],
            # NOVA FUNCIONALIDADE: Informações sobre colunas
            'columns_added': comparison_result['columns_added'],
            'columns_removed': comparison_result['columns_removed'],
            'tables': {
                'new_rows': [],
                'removed_rows': [],
                'modified_rows': []
            }
        }
        
        # Formata linhas novas
        for row in comparison_result['new_rows']:
            formatted_row = {'key': row['key']}
            formatted_row.update(row['data'])
            formatted['tables']['new_rows'].append(formatted_row)
        
        # Formata linhas removidas
        for row in comparison_result['removed_rows']:
            formatted_row = {'key': row['key']}
            formatted_row.update(row['data'])
            formatted['tables']['removed_rows'].append(formatted_row)
        
        # Formata linhas modificadas
        for row in comparison_result['modified_rows']:
            # Identifica quais campos foram alterados
            changes = {}
            for field in row['old_data']:
                if row['old_data'][field] != row['new_data'].get(field):
                    changes[field] = {
                        'old': row['old_data'][field],
                        'new': row['new_data'].get(field)
                    }
            
            formatted_row = {
                'key': row['key'],
                'changes': changes
            }
            formatted['tables']['modified_rows'].append(formatted_row)
        
        return formatted
    
    def generate_summary_text(self, comparison_result: Dict) -> str:
        """
        Gera um resumo textual da comparação.
        
        Args:
            comparison_result: Resultado da comparação
            
        Returns:
            String com o resumo
        """
        summary = comparison_result['summary']
        
        text = f"Comparação concluída:\n"
        text += f"- Arquivo 1: {summary['total_rows_file1']} linhas\n"
        text += f"- Arquivo 2: {summary['total_rows_file2']} linhas\n"
        text += f"- Linhas novas: {summary['new_rows']}\n"
        text += f"- Linhas removidas: {summary['removed_rows']}\n"
        text += f"- Linhas alteradas: {summary['modified_rows']}\n"
        text += f"- Linhas inalteradas: {summary['unchanged_rows']}\n"
        # NOVA FUNCIONALIDADE: Resumo das colunas
        text += f"- Colunas adicionadas: {summary['columns_added']}\n"
        text += f"- Colunas removidas: {summary['columns_removed']}"
        
        return text