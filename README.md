# DCM2TIF
Para poder ejecutar el código se necesita de las siguientes librerias
```
opencv-python   4.4.0.46
pydicom         2.1.1
scikit-image    0.16.2
SimpleITK       2.0.2
tqdm            4.54.1
```
También se puede crear un ambiente virtual con conda, mediante el archivo .yml, 
solo es necesario ejecutar el comando
```
conda env create -f environment.yml
```
Para poder ejecutar el codigo, solo sera necesario ubicarse en la carpeta donde se
encuantra el archivo .py y el comando:
```
python Read_dcm.py --data <Path to dcm files>
```
El codigo buscará todos los archivos que concluyan en .dcm o .DCM, para 
posteriormente leerlos y convertirlos a .tif

Tambien se pueden haceptar los siguientes argumentos opcionales:
```
--width <new_width>
--height <new_height>
--wh <new_shape>
```
se aceptan enteros como valores y la funcion de estos argumentas es hacer internamente 
un reshape al arreglo obtenido de los archivos .dcm, de modo que es posible modificar 
de forma independiente el alto y ancho de la imagen resultante.
