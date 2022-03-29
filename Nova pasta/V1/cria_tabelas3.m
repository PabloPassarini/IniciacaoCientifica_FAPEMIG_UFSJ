function [dadosn,dados] = cria_tabelas3(cidade)
    
    [ano,mes,dia] = datevec(cidade{1,1});
    inicio = ano;
    [a,~] = size(cidade);
    [ano,mes,dia]=datevec(cidade{a,1});
    fim = ano;%definir ano de termino
    dados = [];
    cont = 1;
    for i = inicio:fim
        for j = 1:12
            if j==2
                for k=1:28
                    dados(cont,1) = k;
                    dados(cont,2) = j;
                    dados(cont,3) = i;
                    cont=cont +1;
                end
            elseif j==4 || j==6 || j==9 || j==11
                for k=1:30
                    dados(cont,1) = k;
                    dados(cont,2) = j;
                    dados(cont,3) = i;
                    cont=cont +1;
                end
            else
                for k=1:31
                    dados(cont,1) = k;
                    dados(cont,2) = j;
                    dados(cont,3) = i;
                    cont=cont +1;
                end
                
            end
            
        end
    end
    j=1;
    [m,n] = size(cidade);
    cont = 1;
    for i=1:length(dados)
        cont = j;
        while cont<=m
            [ano,mes,dia] = datevec(cidade{cont,1});
            if ano == dados(i,3) && mes == dados(i,2) && dia == dados(i,1)
               dados(i,4) = cidade{cont,2}; 
               dados(i,5) = cidade{cont,3};
               dados(i,6) = cidade{cont,4};
               dados(i,7) = cidade{cont,5};
               dados(i,8) = cidade{cont,6};
               dados(i,9) = cidade{cont,7};
               dados(i,10) = cidade{cont,8};
               dados(i,11) = cidade{cont,9};
               j=cont+1;
               cont = 100000;
               break;
            else
              
               dados(i,4) = -99; 
               dados(i,5) = -99;
               dados(i,6) = -99;
               dados(i,7) = -99;
               dados(i,8) = -99;
               dados(i,9) = -99;
               dados(i,10) = -99;
               dados(i,11) = -99;
            end
            cont = cont + 1;
        end
    end
    
%% para deletar dados faltantes
%     m = 1;
%     while m <= length(dados)
%         for n = 2:length(dados(1,:))
%             if dados(m,n) == -99
%                 dados(m,:) = [];
%                 m = m - 1;
%                 break
%             end
%         end
%         m = m + 1;
%     end  
    
%% Para normalizar os dados    
%     for i = 1:length(dados(1,:))
%     dadosn(:,i) = ((dados(:,i) - min(dados(:,i)))/(max(dados(:,i)) - min(dados(:,i)))) * 0.6 + 0.2;%normalizaçao dos dados, para que todos os dados tenham o mesmo peso
%     end

end