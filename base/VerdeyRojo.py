import cv2
import numpy as np
fov = 60.0 
# Abre la cámara
cap = cv2.VideoCapture(1)

#es otra forma de dibujar esta añade un borde azul
def dibujar(mask,color):
  contornos,hierachy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  for c in contornos:
    area = cv2.contourArea(c)
    if area > 3000:
      M = cv2.moments(c)
      if (M["m00"]==0): M["m00"]=1
      x = int(M["m10"]/M["m00"])
      y = int(M['m01']/M['m00'])
      nuevoContorno = cv2.convexHull(c)
      cv2.circle(frame,(x,y),7,(0,255,0),-1)
      # cv2.putText(cv2.flip(frame,1),'{},{}'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
      #cv2.putText(cv2.flip(frame,1), 'Texto sin voltear', (50, 50), font, 1, (0, 255, 0), 2)

      cv2.drawContours(frame, [nuevoContorno], -1, (255, 0, 0), 3)

def calcular_distancia(contorno,ancho):
    # Debes realizar una calibraci�n para convertir de p�xeles a unidades de distancia (por ejemplo, cent�metros).
    # Esto implica conocer la distancia real a la que se encuentra el objeto y medir su tama�o en la imagen.
    # Luego, puedes usar la f�rmula de semejanza de tri�ngulos para calcular la distancia.

    # Ejemplo de calibraci�n ficticia (debes ajustar esto con tus propias mediciones)
    distancia_real = 10.0  # Distancia en cent�metros
    ancho_real = 10.0  # Ancho real del objeto en cent�metros
    ancho_pixel = 100  # Ancho del objeto en p�xeles en la imagen

    # Calcula la distancia en cent�metros
    distancia = (ancho_real * ancho_pixel) / (2 * ancho_real * np.tan(fov / 2))
    print(ancho)
    return distancia

while True:
    # Captura un fotograma de la cámara
    ret, frame = cap.read()

    if not ret:
        break

    # Convierte el fotograma a espacio de color HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    anchoVerde = 0
    # Define el rango de colores rojo en HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    #test_red
    redBajo1 = np.array([0,100,20],np.uint8)
    redAlto1 = np.array([5,255,255],np.uint8)
    redBajo2 = np.array([175,100,20],np.uint8)
    redAlto2 = np.array([179,255,255],np.uint8)
    maskRed1 = cv2.inRange(hsv,redBajo1,redAlto1)
    maskRed2 = cv2.inRange(hsv,redBajo2,redAlto2)
    maskRed = cv2.add(maskRed1,maskRed2)
    dibujar(maskRed,(0,0,255))
                                                              

    # Define el rango de colores verde en HSV
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])

    # Crea máscaras para los colores rojo y verde
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Encuentra los contornos de los objetos rojos y verdes
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dibuja contornos y rellena con el color respectivo
    for contour in contours_red:
        area = cv2.contourArea(contour)
        if area > 3000:
            M = cv2.moments(contour)
            if (M["m00"]==0): M["m00"]=1
            x = int(M["m10"]/M["m00"])
            y = int(M['m01']/M['m00'])
            cv2.circle(frame, (x,y), 7, (0,255,0), -1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, '{},{}'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
            nuevoContorno = cv2.convexHull(contour)
            x, y, w, h = cv2.boundingRect(nuevoContorno)
            cv2.drawContours(frame, [nuevoContorno], -1, (0, 0, 255), 3)
    # cv2.drawContours(frame, [contour], -1, (0, 0, 255), 5)  # Rojo
    
    for contour in contours_green:
        area = cv2.contourArea(contour)
        if area > 3000:
            M = cv2.moments(contour)
            if (M["m00"]==0): M["m00"]=1
            x = int(M["m10"]/M["m00"])
            y = int(M['m01']/M['m00'])
            cv2.circle(frame, (x,y), 7, (0,255,0), -1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, '{},{}'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
            nuevoContorno = cv2.convexHull(contour)
            x, y, w, h = cv2.boundingRect(nuevoContorno)
            anchoVerde = w
            cv2.drawContours(frame, [nuevoContorno], -1, (0, 255, 0), 3)
        # cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)  # Verde

    # Calcula la distancia al objeto detectado (debes calibrar esta parte)
    distancia_rojo = calcular_distancia(contours_red,2)
    distancia_verde = calcular_distancia(contours_green,anchoVerde)

    # Imprime la distancia en la consola
    # print(f'Distancia al objeto rojo: {distancia_rojo} cm')
    
    # print(f'Distancia al objeto verde: {distancia_verde} cm')

    # Muestra el fotograma
    cv2.imshow('Detección de colores', frame)

    # Detiene el bucle si se presiona la tecla 's'
    if cv2.waitKey(50) & 0xFF == ord('s'):
        break

# Libera la cámara y cierra las ventanas
cap.release()
cv2.destroyAllWindows()
