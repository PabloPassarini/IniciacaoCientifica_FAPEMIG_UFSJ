% indl = 40% dataset for learners training
% indm = 40% dataset for meta-learners training
% indp = 20% dataset for validation
% learnersV = number of ML's
% learners -> function with ML's
% metaLearnersV = number of meta-learners
% metaLearners -> function with meta-learners
% triangulationMethodsV = number of triangulation methods
% triangulationMethods = function with the triangulation methods

%% Pra executar vc precisa ter o arquivo com o nome MLdata 

% Para normalizar os dados    
for i = 1:length(MLdata(1,:))
    MLdata(:,i) = ((MLdata(:,i) - min(MLdata(:,i)))/(max(MLdata(:,i)) - min(MLdata(:,i)))) * 0.6 + 0.2;%normalizaçao dos dados, para que todos os dados tenham o mesmo peso
end

indl = 1:(round(size(MLdata,1)*0.4));
indm = (round(size(MLdata,1)*0.4)):(round(size(MLdata,1)*0.8));
indp = (round(size(MLdata,1)*0.8)):(round(size(MLdata,1)*1));
learnersV = 3;
metaLearnersV = 3;
M1=[];
P1=[];


    for j=1:(learnersV)
            [l,c]=size(MLdata);
            for k=4%(c-3)
                L = mlData(k,MLdata(indl,:));
                M = mlData(k,MLdata(indm,:));
                P = mlData(k,MLdata(indp,:));
                model = learners(j,L);
                [~,colunas] = size(M);
                switch (j)
                    case 1
                        M1 = [M1;M(:,(colunas-3):(colunas-1)) predict(model,M(:,1:(colunas-1)))];
                        P1 = [P1;P(:,(colunas-3):(colunas-1)) predict(model,P(:,1:(colunas-1)))];
                    case 2
                        M1 = [M1;M(:,(colunas-3):(colunas-1)) model(M(:,1:(colunas-1))')'];
                        P1 = [P1;P(:,(colunas-3):(colunas-1)) model(P(:,1:(colunas-1))')'];
                    case 3
                        M1 = [M1;M(:,(colunas-3):(colunas-1)) predict(model,M(:,1:(colunas-1)))];
                        P1 = [P1;P(:,(colunas-3):(colunas-1)) predict(model,P(:,1:(colunas-1)))];
                end
            end 
        end