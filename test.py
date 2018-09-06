import adaboost as ada
model = ada.load('classifier_model/h32c100/accessoryHat.pkl')
ada.exportgraphviz(model,'ad')