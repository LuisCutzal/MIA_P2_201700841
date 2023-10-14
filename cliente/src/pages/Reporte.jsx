import Tarjeta from "./Tarjeta";

const Reporte = () => {
    const imagenes = [
        'https://picsum.photos/id/102/4320/3240',
        'https://picsum.photos/id/103/2592/1936',
        'https://picsum.photos/id/104/3840/2160',
        'https://picsum.photos/id/106/2592/1728',
        'https://picsum.photos/id/107/5000/3333',
        'https://picsum.photos/id/107/5000/3333',
        'https://picsum.photos/id/107/5000/3333',
        'https://picsum.photos/id/107/5000/3333',
        'https://picsum.photos/id/107/5000/3333',
        'https://picsum.photos/id/107/5000/3333',
        'https://picsum.photos/id/107/5000/3333',
        'https://picsum.photos/id/107/5000/3333',
    ];
    return (
        <div className="text-center">
            <h1 className="text-2xl font-bold text-white ">Reportes</h1>
            <div className="grid grid-cols-3 gap-4">
                {imagenes.map((imagen, index) => (
                    <Tarjeta key={index} imagenSrc={imagen} />
                ))}
            </div>
        </div>
    );
};
export default Reporte