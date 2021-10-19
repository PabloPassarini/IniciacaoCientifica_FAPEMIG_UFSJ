function [MLdata] = mlData(select, dados)

%% Escolhendo indicador foco, 8 indicadores totais

switch (select)
    
    case 1
        ind = 'precipitacao';
        pos = 4; %posição do indicador 
    case 2
        ind = 'tmax';
        pos = 5; %posição do indicador 
    case 3 
        ind = 'tmed';
        pos = 6; %posição do indicador 
    case 4
        ind = 'tmin';
        pos = 7; %posição do indicador 
    case 5
        ind = 'umidadeRelativa';
        pos = 8; %posição do indicador 
    
end

date = dados(:,1:3);
MLdata = [date dados(:,pos)];


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
                MLdata(i,4+(n_entradas*j)) = dados(i+j,pos);
            else
                MLdata(i,1+(n_entradas*j)) = dados(i+j,1);
                MLdata(i,2+(n_entradas*j)) = dados(i+j,2);
                MLdata(i,3+(n_entradas*j)) = dados(i+j,3);
                MLdata(i,4+(n_entradas*j)) = dados(i+j,pos);
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