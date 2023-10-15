
const Tarjeta = ({ imagenSrc, nombreImagen }) => {
  return (
    <a href={imagenSrc} download={nombreImagen} className="bg-primary" >
    <div className="bg-primary w-50 h-30 m-2 p-4 border-4 border-gray-500 rounded-lg text-center ">
      <img src={imagenSrc} alt={nombreImagen} className="w-full h-full" />
      <div className="text-sm mt-2">{nombreImagen}</div>
    </div>
    </a>
  );
};

export default Tarjeta;
