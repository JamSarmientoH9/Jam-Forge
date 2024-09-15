"""
data_preprocessing.py

Este módulo contiene la clase DataPreprocessor, que se encarga de cargar,
preprocesar y guardar datos para el proyecto de chatbot de WhatsApp.

"""

import json
import pandas as pd
from nlp_utils import TextProcessor

class DataPreprocessor:
    """
    Clase para preprocesar datos para el chatbot de WhatsApp.

    Esta clase proporciona métodos para cargar datos desde archivos JSON o CSV,
    preprocesar texto utilizando un TextProcessor, y guardar los resultados.
    """

    def __init__(self, text_processor=None):
        """
        Inicializa el DataPreprocessor.

        Args:
            text_processor (TextProcessor, opcional): Instancia de TextProcessor para procesar texto.
                Si no se proporciona, se crea una nueva instancia.
        """
        self.text_processor = text_processor if text_processor else TextProcessor()

    def load_data(self, file_path, file_type='json'):
        """
        Carga datos desde un archivo.

        Args:
            file_path (str): Ruta al archivo de datos.
            file_type (str): Tipo de archivo ('json' o 'csv'). Por defecto es 'json'.

        Returns:
            list: Lista de diccionarios con los datos cargados.

        Raises:
            FileNotFoundError: Si el archivo no se encuentra.
            ValueError: Si el tipo de archivo no es soportado.
        """
        try:
            if file_type == 'json':
                with open(file_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            elif file_type == 'csv':
                df = pd.read_csv(file_path)
                if df.empty:
                    print("Advertencia: el archivo CSV está vacío.")
                return df.to_dict('records')
            else:
                raise ValueError("Tipo de archivo no soportado. Use 'json' o 'csv'.")
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {file_path}.")
            raise
        except json.JSONDecodeError:
            print(f"Error: El archivo {file_path} no es un JSON válido.")
            raise

    def preprocess_data(self, data, text_field):
        """
        Preprocesa el texto en el campo especificado de los datos.

        Args:
            data (list): Lista de diccionarios con los datos.
            text_field (str): Nombre del campo que contiene el texto a preprocesar.

        Returns:
            list: Datos con el texto preprocesado.
        """
        for item in data:
            if text_field in item:
                item[text_field] = self.text_processor.preprocess(item[text_field])
            else:
                print(f"Advertencia: '{text_field}' no encontrado en el item: {item}")
        return data

    def save_data(self, data, output_file, file_type='json'):
        """
        Guarda los datos procesados en un archivo.

        Args:
            data (list): Datos a guardar.
            output_file (str): Ruta del archivo de salida.
            file_type (str): Tipo de archivo ('json' o 'csv'). Por defecto es 'json'.

        Raises:
            ValueError: Si el tipo de archivo no es soportado.
        """
        try:
            if file_type == 'json':
                with open(output_file, 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=2, ensure_ascii=False)
            elif file_type == 'csv':
                df = pd.DataFrame(data)
                df.to_csv(output_file, index=False, encoding='utf-8')
            else:
                raise ValueError("Tipo de archivo no soportado. Use 'json' o 'csv'.")
            print(f"Datos procesados guardados en {output_file}")
        except Exception as e:
            print(f"Ocurrió un error al guardar los datos: {e}")
            raise

    def prepare_data(self, input_file, output_file, text_field='text', input_type='json', output_type='json'):
        """
        Función principal para preparar y procesar datos.

        Args:
            input_file (str): Ruta del archivo de entrada.
            output_file (str): Ruta del archivo de salida.
            text_field (str): Nombre del campo de texto a procesar. Por defecto es 'text'.
            input_type (str): Tipo de archivo de entrada ('json' o 'csv'). Por defecto es 'json'.
            output_type (str): Tipo de archivo de salida ('json' o 'csv'). Por defecto es 'json'.
        """
        data = self.load_data(input_file, file_type=input_type)
        processed_data = self.preprocess_data(data, text_field)
        self.save_data(processed_data, output_file, file_type=output_type)

    def get_unique_values(self, data, field):
        """
        Obtiene valores únicos en un campo específico de los datos.

        Args:
            data (list): Lista de diccionarios con los datos.
            field (str): Nombre del campo del cual obtener valores únicos.

        Returns:
            list: Lista de valores únicos en el campo especificado.
        """
        return list(set(item[field] for item in data if field in item))

    def filter_data(self, data, condition):
        """
        Filtra los datos basándose en una función de condición.

        Args:
            data (list): Lista de diccionarios con los datos.
            condition (callable): Función que toma un item y devuelve True si debe incluirse.

        Returns:
            list: Lista filtrada de datos.
        """
        return [item for item in data if condition(item)]

    def add_field(self, data, field_name, value_function):
        """
        Añade un nuevo campo a cada item en los datos.

        Args:
            data (list): Lista de diccionarios con los datos.
            field_name (str): Nombre del nuevo campo a añadir.
            value_function (callable): Función que toma un item y devuelve el valor para el nuevo campo.

        Returns:
            list: Datos con el nuevo campo añadido.
        """
        for item in data:
            item[field_name] = value_function(item)
        return data

# Ejemplo de uso
if __name__ == "__main__":
    preprocessor = DataPreprocessor()
    
    # Preparar datos
    preprocessor.prepare_data('input_data.json', 'processed_data.json', text_field='message')
    
    # Cargar datos procesados
    processed_data = preprocessor.load_data('processed_data.json')
    
    # Obtener valores únicos
    unique_senders = preprocessor.get_unique_values(processed_data, 'sender')
    print("Remitentes únicos:", unique_senders)
    
    # Filtrar datos
    important_messages = preprocessor.filter_data(processed_data, lambda x: 'importante' in x['message'].lower())
    print("Número de mensajes importantes:", len(important_messages))
    
    # Añadir un nuevo campo
    data_with_length = preprocessor.add_field(processed_data, 'message_length', lambda x: len(x['message']))
    print("Primer item con longitud de mensaje:", data_with_length[0])
