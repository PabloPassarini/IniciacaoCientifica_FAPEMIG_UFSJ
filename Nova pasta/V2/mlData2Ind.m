function [MLdata] = mlData2Ind(select, dados)

%% Escolhendo indicador foco, 8 indicadores totais

switch (select)
    
    case 1
        ind = 'precipitacao';
        posi = 5;
        posf = 4; %posição do indicador 
    case 2
        ind = 'precipitacao';
        posi = 6;
        posf = 4; %posição do indicador 
    case 3 
        ind = 'precipitacao';
        posi = 7;
        posf = 4; %posição do indicador  
    case 4
        ind = 'precipitacao';
        posi = 8;
        posf = 4; %posição do indicador 
        
        
    case 5
        ind = 'tmax';
        posi = 4;
        posf = 5; %posição do indicador 
    case 6
        ind = 'tmax';
        posi = 6;
        posf = 5; %posição do indicador  
    case 7 
        ind = 'tmax';
        posi = 7;
        posf = 5; %posição do indicador  
    case 8
        ind = 'tmax';
        posi = 8;
        posf = 5; %posição do indicador 
        
        
    case 9
        ind = 'tmed';
        posi = 4;
        posf = 6; %posição do indicador 
    case 10
        ind = 'tmed';
        posi = 5;
        posf = 6; %posição do indicador  
    case 11
        ind = 'tmed';
        posi = 7;
        posf = 6; %posição do indicador 
    case 12
        ind = 'tmed';
        posi = 8;
        posf = 6; %posição do indicador  
   
        
    case 13
        ind = 'tmin';
        posi = 4;
        posf = 7; %posição do indicador 
    case 14
        ind = 'tmin';
        posi = 5;
        posf = 7; %posição do indicador 
    case 15 
        ind = 'tmin';
        posi = 6;
        posf = 7; %posição do indicador  
    case 16
        ind = 'tmin';
        posi = 8;
        posf = 7; %posição do indicador 
        
        
    case 17
        ind = 'umidadeRelativa';
        posi = 4;
        posf = 8; %posição do indicador
    case 18
        ind = 'umidadeRelativa';
        posi = 5;
        posf = 8; %posição do indicador
    case 19
        ind = 'umidadeRelativa';
        posi = 6;
        posf = 8; %posição do indicador
    case 20
        ind = 'umidadeRelativa';
        posi = 7;
        posf = 8; %posição do indicador
    
end

date = dados(:,1:3);
MLdata= [date dados(:,posi) dados(:,posf)];


%% Preparar Matriz para Machine Learning

conjunto = 5;%tamanho da janela deslizante
n_entradas = 5;
    
    entrou = 0;
    cont = 1;
    MLdata = [];
    
    for i=1:length(dados)-(conjunto-1)
        
        for j=0:conjunto-1 
            if j==conjunto-1
                MLdata(i,1+(n_entradas*j)) = dados(i+j,1);
                MLdata(i,2+(n_entradas*j)) = dados(i+j,2);
                MLdata(i,3+(n_entradas*j)) = dados(i+j,3);
                MLdata(i,4+(n_entradas*j)) = dados(i+j,posi);
                MLdata(i,5+(n_entradas*j)) = dados(i+j,posf);
            else
                MLdata(i,1+(n_entradas*j)) = dados(i+j,1);
                MLdata(i,2+(n_entradas*j)) = dados(i+j,2);
                MLdata(i,3+(n_entradas*j)) = dados(i+j,3);
                MLdata(i,4+(n_entradas*j)) = dados(i+j,posi);
                MLdata(i,5+(n_entradas*j)) = dados(i+j,posf);
            end
        end
    end
    
    m = 1;
    while m <= length(MLdata)
        for n = 2:length(MLdata(1,:))
            if isnan(MLdata(m,n))
                MLdata(m,:) = [];
                m = m - 1;
                break
            end
        end
        m = m + 1;
    end
end