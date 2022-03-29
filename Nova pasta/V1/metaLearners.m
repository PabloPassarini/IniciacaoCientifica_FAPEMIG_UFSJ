function [model] = metaLearners(select, dados)

%% Pre-processing 
trainInd = [];
testInd = [];
trainX = [];
testX = [];
testXn = [];
Realn = [];
Real = [];
trainTempMax = [];
newTrainX = [];
newTestX = [];
   
[a,b] = size(dados);
conjunto = 0; %tamanho da janela deslizante
% multiplicador = (a-(3))/a;%(a-31)/a;   

%[trainInd,~,testInd] = dividerand(size(dadosn,1),0.6,0,0.3);
trainInd = 1:(round(size(dados,1)));
testInd = (round(size(dados,1))+1):size(dados,1);
% trainInd = 1:(round(size(dadosn,1)*0.8));% 48 meses
% testInd = (round(size(dadosn,1)*0.8)+1):size(dadosn,1);
trainX = dados(trainInd,:);
testX = dados(testInd,:);
Realn = testX(:,b);            %Real normalizado

trainTempMax = trainX(:,b);
newTrainX = [removerows(trainX','ind',b)]';
newTestX = [removerows(testX','ind',b)]';


switch (select)
    case 1 
        %% TB
        mdl_TB = TreeBagger(30,newTrainX,trainTempMax,'Method','regression','NumPredictorsToSample', 'all');
        %mdl_TB = TreeBagger(200,newTrainX,trainTempMax,'Method','regression','Surrogate','on',...
        %'PredictorSelection','curvature','OOBPredictorImportance','on');
        model = mdl_TB;
        
    case 2
        %% NN
        trainFcn = 'trainbfg';  %Bayesian Regularization backpropagation. trainlm, trainbfg, trainbr
        hiddenLayerSize = 4;
        net = fitnet(hiddenLayerSize,trainFcn);
        net.divideParam.trainRatio = 80/100;
        net.divideParam.valRatio = 20/100;
        %net.divideParam.testRatio = 15/100;
        net.performFcn = 'sse';% calcular erro
        net.trainParam.showWindow = 0;

        mdl_NN = train(net,newTrainX',trainTempMax');
        
    case 3
        %% SVM
        mdl_SVM = fitrsvm(newTrainX,trainTempMax,'KernelFunction','gaussian',...
        'KernelScale','auto','Standardize',true, 'BoxConstraint', 0.1, 'epsilon', 2*10^-6);%'epsilon', 2*10^-6(0.0009),'BoxConstraint', 0.1(0.25)

end

end