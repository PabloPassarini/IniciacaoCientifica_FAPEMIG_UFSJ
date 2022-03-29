function [methodRes] = triangulationMethods(select, data)
aux=[];
data=triangulationData(4,data);
methodRes=[];
%% Coordinates 
bh = [-19.93444 -43.952222];
florestal = [-19.99542 -44.416889];
d1 = haversine(bh,florestal);
ibirite = [-20.0166 -44.084722];
d2 = haversine(bh,ibirite);
seteLagoas = [-19.48454 -44.173798];
d3 = haversine(bh, seteLagoas);
d = [d1 d2 d3];
%% Altitude
bhA = 0.91547;
florestalA = 0.75351;
ibiriteA = 0.82208;
seteLagoasA = 0.75368;
altitude = [bhA florestalA ibiriteA seteLagoasA];

%% IMAD -> indicator monthly average dataset
iMAD = []; 
cont=1;
        for i=1:length(data)-1
            if data(i,2) == data(i+1,2)
                aux = [aux;data(i,:)];       
            else
                iMAD = [iMAD;aux(1,2:3) mean(aux(:,4)) mean(aux(:,5)) mean(aux(:,6)) mean(aux(:,7))];
                cont=cont+1;
                aux=[];
            end
        end

switch (select)
    
    case 1
        %% Arithmetic Average
        for i=1:length(data)
            methodRes = [methodRes; data(i,1:3) mean(data(i,5:7))];
        end
        
    case 2
        %% Inverse Distance Weighted
        for i=1:length(data)
            methodRes = [methodRes;data(i,1:3) ((data(i,5)/d1 + data(i,6)/d2 + data(i,7)/d3) / ( 1/d1 + 1/d2 + 1/d3))];
        end
        
    case 3
        %% Optimized Inverse Distance Weighted
        cont = 1;
        aux = 1;
        while cont<=length(iMAD)
            
            if data(aux,2) == iMAD(cont,1)
%                 yi_di = ((data(aux,5)/d1 + data(aux,6)/d2 + data(aux,7)/d3));
%                 a_ai = (iMAD(cont,3)/iMAD(cont,4) + iMAD(cont,3)/iMAD(cont,5) + iMAD(cont,3)/iMAD(cont,6));
%                 logh_loghi = (log(bhA)/log(florestalA) + log(bhA)/log(ibiriteA) + log(bhA)/log(seteLagoasA));
%                 Idi = ( 1/d1 + 1/d2 + 1/d3);
%                 teste(1) = (data(aux,5)/d1 * iMAD(cont,3)/iMAD(cont,4) * log(bhA)/log(florestalA))/(1/d1);
%                 teste(2) = (data(aux,6)/d2 * iMAD(cont,3)/iMAD(cont,5) * log(bhA)/log(ibiriteA))/(1/d2);
%                 teste(3) = (data(aux,7)/d3 * iMAD(cont,3)/iMAD(cont,6) * log(bhA)/log(seteLagoasA))/(1/d3);

                % for para calcular os resultados de cada n do somatorio
                for i=1:3 % de 1 ate o numero de cidades vizinhas
                    vecSum(i) = (data(aux,4+i)/d(i) * iMAD(cont,3)/iMAD(cont,3+i) * log(altitude(1))/log(altitude(1+i)))/(1/d(i));
                end
                
                methodRes = [methodRes; data(aux,1:3) (sum(vecSum))];
                aux = aux + 1;
            else
                cont=cont+1;
            end
        end
                
    case 4
        %% Optimized Normal Ratio
        monthlyCorrelation=[];
        for i=1:length(data)-1
            if data(i,2) == data(i+1,2)
                aux = [aux;data(i,:)];       
            else
                r1 = corrcoef(aux(:,4),aux(:,5));
                r2 = corrcoef(aux(:,4),aux(:,6));
                r3 = corrcoef(aux(:,4),aux(:,7));
                monthlyCorrelation = [monthlyCorrelation;aux(1,2:3) r1(1,2) r2(1,2) r3(1,2)];
                aux=[];
            end
        end
        correction = monthlyCorrelation(1,:);
        monthlyCorrelation(1,:)=[];
        monthlyCorrelation(length(monthlyCorrelation),:) = correction;
        cont = 1;
        aux = 1;
        aux2 = 0;
        while cont<length(monthlyCorrelation)-1
            
            if data(aux,2) == monthlyCorrelation(cont,1)
                    
               for j=1:3 % de 1 ate o numero de cidades vizinhas
                   vecSum= (data(aux,4+j) * ( monthlyCorrelation(cont,2+j)^(2*((30-2)/(1-monthlyCorrelation(cont,2+j)^2)))) ) / ( monthlyCorrelation(cont,2+j)^(2*((30-2)/(1-monthlyCorrelation(cont,2+j)^2))));    
               end

                methodRes = [methodRes; data(aux,1:3) sum(vecSum)];
                aux=aux+1;
            else
                cont=cont+1;
            end
        end
    case 5  
        %% Regional Weight
        
        cont = 1;
        aux = 1;
        while cont<=length(iMAD)
            
            if data(aux,2) == iMAD(cont,1)
                
                for i=1:3 % de 1 ate o numero de cidades vizinhas
                    vecSum(i) = ( ( iMAD(cont,3)/iMAD(cont,3+i) ) * data(aux,4+i) );
                end
                
                methodRes = [methodRes; data(aux,1:3) sum(vecSum)/3];
                aux=aux+1;
            else
                cont=cont+1;
            end
        end
end





end