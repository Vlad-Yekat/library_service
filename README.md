# library_service
Python/Django library microservice
with JSON RPC 2.0 

# Входной запрос типа
    {
     "jsonrpc": "2.0",
     "method": "add_writer",
     "params": {
                "name": "Karl",
                "surname": "Marks",
                ...
                },
     "id": 3
    }
 и возвращает
 
     {"jsonrpc": "2.0", "result": 1, "id": 3}
  
  добавляет автора

а

    {
     "jsonrpc": "2.0",
     "method": "add_book",
     "params": {"writer_id" :1
                "title": "Capital",
                ...
                },
     "id": 3
    }
    
 возвращает
 
    {"jsonrpc": "2.0", "result": 1, "id": 3}
  
  добавляет книгу
  итд
  

