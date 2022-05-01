from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionGuardarNombre(Action):
    def name(self) -> Text:
        return "action_guardar_nombre"
    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        nombre = next(tracker.get_latest_entity_values("nombre"), None)
        text = str(nombre)
        
        message=f"Un placer conocerle {text}, en que puedo auyudarle?"
        dispatcher.utter_message(text=str(message))
        
        return [SlotSet("nombre",text)]      

# Desformatea el tamaño de un room y envía el mensaje para que sea utilizado en Unity
class ActionGuardarTamanio(Action):
    def name(self) -> Text:
        return "action_guardar_tamanio"  

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tamanio_room = str(tracker.get_slot("tamanio_room"))
            
        arreglo_tamanio = tamanio_room.split("x")
        tamanio_x = arreglo_tamanio[0] 
        tamanio_z = arreglo_tamanio[1]
        
        dispatcher.utter_message(text = "Crear room," + tamanio_x + "," + tamanio_z)
        return [SlotSet("tamanio_x", tamanio_x), SlotSet("tamanio_z", tamanio_z)]  

class ActionGuardarObjeto(Action):
    """ 
        Obtiene el objeto a crear y la cantidad de los slots. Luego, desformatea las posiciones, 
        verificando que la cantidad obtenida sea igual al número de objetos a crear. Por último, obtiene las posiciones específicas
        y emite un mensaje." 
    """
    def name(self) -> Text:
        return "action_guardar_objeto"  

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        objeto = str(tracker.get_slot("objeto"))
        cantidad = tracker.get_slot("cantidad")
       
        posicion = str(tracker.get_slot("posicion"))
        posicion = posicion.replace(" ", "")
        
        arreglo_posicion = posicion.split(";")
        
        if(len(arreglo_posicion) != int(cantidad)):
            dispatcher.utter_message(text="Al parecer ingresó una cantidad diferente de posiciones a la cantidad de objetos especificada")
            return [SlotSet("posicion", None)]  

        for pos in arreglo_posicion:    
            
            pos = str(pos)
            pos_x = pos.split(",")[0]
            pos_z = pos.split(",")[1]
            dispatcher.utter_message(text = "Crear objeto," + objeto + "," + pos_x + "," + pos_z)
        
        return []  
     
class ActionDeterminarRoom(Action):
        def name(self) -> Text: 
            return "action_determinar_room"  

        def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            tema_microlearning = str(tracker.get_slot("tema_microlearning"))
            
            if(tema_microlearning == "crear un room"):
                dispatcher.utter_message(text = "Crear room," + "20"+ "," + "20")
                return[]

            #tal vez tener un mapa donde las claves sean los temas y los valores sean los tipos de rooms
            room_microlearning = "RoomBanco"
            dispatcher.utter_message(text = "Room microlearning," + room_microlearning + "," + tema_microlearning)
            return[]
        
