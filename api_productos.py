from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4 as ud

app=FastAPI()


class Producto(BaseModel):
    
    id : Optional[str]= None
    nombre : str
    precio_compra : float
    precio_venta : float
    proveedor : str
    
    
productos=[]

@app.get('/')
def index():
    return {"Welcome to the product API"}

@app.get('/producto')
def obtener_productos():
    return productos

@app.post('/producto')
def crear_producto(producto: Producto):
    producto.id = str(ud())
    productos.append(producto)
    return {'Product created'}

@app.get('/producto/{producto_id}')
def producto_por_id(producto_id : str):
    resultado=list(filter(lambda p:p.id ==producto_id, productos))
    if len(resultado):
        return resultado
    raise HTTPException(status_code=404, detail=f'El producto con el ID {producto_id} no fue encontrado.')   

@app.delete('/producto/{producto_id}')
def eliminar_producto_por_id(producto_id : str):
    resultado=list(filter(lambda p:p.id ==producto_id, productos))
    if len(resultado):
        producto = resultado[0]
        productos.remove(producto)
        return {f'El producto cuya ID es {producto_id} fue eliminado'}
    raise HTTPException(status_code=404, detail=f'El producto con el ID {producto_id} no fue encontrado.')  

@app.put('/producto/{producto_id}')
def actualizar_producto_por_id(producto_id : str, producto : Producto):
    resultado=list(filter(lambda p:p.id ==producto_id, productos))
    
    if len(resultado):
        producto_en = resultado[0]
        producto_en.nombre = producto.nombre
        producto_en.precio_venta = producto.precio_venta
        producto_en.precio_compra = producto.precio_compra
        producto_en.proveedor = producto.proveedor
        
        return producto_en
    raise HTTPException(status_code=404, detail=f'El producto con el ID {producto_id} no fue encontrado.')