function [results] = predictions(MLdata, TRIAdata)

% indl = 40% dataset for learners training
% indm = 40% dataset for meta-learners training
% indp = 20% dataset for validation
% learnersV = number of ML's
% learners -> function with ML's
% metaLearnersV = number of meta-learners
% metaLearners -> function with meta-learners

indl = 1:(round(size(MLdata,1)*0.4));
indm = (round(size(MLdata,1)*0.4)):(round(size(MLdata,1)*0.8));
indp = (round(size(MLdata,1)*0.8)):(round(size(MLdata,1)*1));
learnersV = 3;
metaLearnersV = 3;
M1=[];
P1=[];

    for i=1:(metaLearnersV)
        for j=1:1%(learnersV)
            [l,c]=size(MLdata);
            for k=1:(c-3)
                L = mlData(k,MLdata(indl,:));
                M = mlData(k,MLdata(indm,:));
                P = mlData(k,MLdata(indp,:));
                model = learners(j,L);
                switch (j)
                    case 1
                        M1 = [M1;M(:,1:3) predict(model,M(:,1:3))];
                        P1 = [P1;P(:,1:3) predict(model,P(:,1:3))];
                    case 2
                        M1 = [M1;M(:,1:3) model(M(:,1:3)')];
                        P1 = [P1;P(:,1:3) model(P(:,1:3)')];
                    case 3
                        M1 = [M1;M(:,1:3) predict(model,M(:,1:3))];
                        P1 = [P1;P(:,1:3) predict(model,P(:,1:3))];
                end
            end 
        end
        T1 = TRIAdata(indm,:);
        T2 = TRIAdata(indp,:);
        M1 = [M1;T1(:,1:3) triangulationMethods(5,T1)];
        P1 = [P1;T2(:,1:3) triangulationMethods(1,T2)];
        metaModel = train(metaLearners(i,M1));
        results(i) = fit(metaModel,P1);
    end
end