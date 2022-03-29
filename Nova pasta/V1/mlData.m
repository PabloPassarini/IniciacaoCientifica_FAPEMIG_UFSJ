function [MLdata] = mlData(select, dados)

%% Escolhendo indicador foco, 8 indicadores totais

switch (select)
    case 1
        ind = 'evaPiche';
        pos = 4; %posição do indicador   
    case 2
        ind = 'insolacao';
        pos = 5; %posição do indicador 
    case 3
        ind = 'precipitacao';
        pos = 6; %posição do indicador 
    case 4
        ind = 'tmax';
        pos = 7; %posição do indicador 
    case 5 
        ind = 'tmed';
        pos = 8; %posição do indicador 
    case 6
        ind = 'tmin';
        pos = 9; %posição do indicador 
    case 7
        ind = 'umidadeRelativa';
        pos = 10; %posição do indicador 
    case 8
        ind = 'ventoVelocidade';
        pos = 11; %posição do indicador 
end

date = dados(:,1:3);
MLdata= [date dados(:,pos)];


% %% Preparar Matriz para Machine Learning
% 
% conjunto = 5;%tamanho da janela deslizante
% n_entradas = 5;
%     
%     entrou = 0;
%     cont = 1;
%     MLdata = [];
%     
%     for i=1:length(dados)-(conjunto-1)
%         
%         for j=0:conjunto-1 
%             if j==conjunto-1
%                 MLdata(i,1+(n_entradas*j)) = dados(i+j,1);
%                 MLdata(i,2+(n_entradas*j)) = dados(i+j,2);
%                 MLdata(i,2+(n_entradas*j)) = dados(i+j,3);
%                 MLdata(i,2+(n_entradas*j)) = dados(i+j,pos);
%             else
%                 MLdata(i,1+(n_entradas*j)) = dados(i+j,1);
%                 MLdata(i,2+(n_entradas*j)) = dados(i+j,2);
%                 MLdata(i,2+(n_entradas*j)) = dados(i+j,3);
%                 MLdata(i,2+(n_entradas*j)) = dados(i+j,pos);
%             end
%         end
%     end
%     
%     m = 1;
%     while m <= length(MLdata)
%         for n = 2:length(MLdata(1,:))
%             if MLdata(m,n) == -1
%                 MLdata(m,:) = [];
%                 m = m - 1;
%                 break
%             end
%         end
%         m = m + 1;
%     end
end