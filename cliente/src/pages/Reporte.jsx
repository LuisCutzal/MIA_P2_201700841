import Tarjeta from "./Tarjeta";
import React, { useState, useEffect } from "react";
const Reporte = () => {
    const [imagenes, setImagenes] = useState([])
    useEffect(() => {
        async function getData() {
            try {
                const response = await fetch("http://127.0.0.1:5000/api/getImages")
                const datos = await response.json()
                setImagenes(datos)
            }
            catch (error) {
                print(error)
            }
        }
        getData()
    },[])
    
    return (
        <div className="text-center bg-primary">
            <h1 className="text-2xl font-bold text-white ">Reportes</h1>
            <div className="grid grid-cols-3 gap-4">
                {imagenes.map((imagen, index) => (
                    <Tarjeta key={index} imagenSrc={imagen.direccion} nombreImagen={imagen.nombre} />
                ))}
            </div>
        </div>
    );
};
export default Reporte