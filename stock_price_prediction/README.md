### Consideraciones a tener sobre el código contenido en esta carpeta:

Los notebooks contenidos en esta carpeta cumplen los siguientes propósitos:
- **nb_spp_model_training.ipynb:** contiene el código base (a manera de template) para hacer entrenamiento, experimentación y registro en MLflow de los modelos de ML a usar en la solución
- **nb_spp_model_prep.ipynb:** contiene el código base (a manera de template) que permite cargar la última versión de los modelos registrados en MLflow, realizar las predicciones de interés y persistir los resultados en el data lake (capa Gold)
- **nb_spp_model_ensemble.ipynb:** contiene el código que nos permitió realizar las predicciones (de precios de acciones) para el periodo de datos definido para el prototipo y demo, a través del ensamble de tres modelos: redes neuronales (CNN), XGBoost y Random Forest.

Como próximos pasos, en caso se decida implementar la solución, el código contenido en estos notebooks es la base para generar los scripts para integrar y automatizar el proceso de: entrenamiento, registro, carga de modelos, predicción, y persistencia de resultados en data lake, usando los modelos propuestos en el ensamble.

Es importante mencionar que todo el código en cuestión fue probado y es 100% funcional.