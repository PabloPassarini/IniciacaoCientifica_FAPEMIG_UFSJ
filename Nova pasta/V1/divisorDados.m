function [tri1,tri2,tri3,tri4] = divisorDados(dados,opcao)

switch (opcao)
    case 1
        
        PrimeiroTri=[];
        for i = 1:length(dados)  
            if dados(i,2)==1 || dados(i,2)==2 || dados(i,2)==3
                PrimeiroTri = [PrimeiroTri;dados(i,:)];
            end
        end


        SegundoTri=[];
        for i = 1:length(dados)  
            if dados(i,2)==4 || dados(i,2)==5 || dados(i,2)==6
                SegundoTri = [SegundoTri;dados(i,:)];
            end     
        end


        TerceiroTri=[];
        for i = 1:length(dados)  
            if dados(i,2)==7 || dados(i,2)==8 || dados(i,2)==9
                TerceiroTri = [TerceiroTri;dados(i,:)]; 
            end
        end


        QuartoTri=[];
        for i = 1:length(dados)  
            if dados(i,2)==10 || dados(i,2)==11 || dados(i,2)==12
                QuartoTri = [QuartoTri;dados(i,:)]; 
            end     
        end

    
    case 2
    
     Janeiro=[];
        for i=1:length(dados)
            if dados(i,2)==1
               Janeiro = [Janeiro;dados(i,:)]; 
            end     
        end
        Janeiro(:,2)=[];

        Fevereiro=[];
        for i=1:length(dados)  
            if dados(i,2)==2
               Fevereiro = [Fevereiro;dados(i,:)]; 
            end     
        end
        Fevereiro(:,2)=[];

        Marco=[];
        i=1;
        for i=1:length(dados) 
            if dados(i,2)==3
               Marco = [Marco;dados(i,:)]; 
            end     
        end
        Marco(:,2)=[];

        Abril=[];
        for i=1:length(dados) 
            if dados(i,2)==4
               Abril = [Abril;dados(i,:)]; 
            end     
        end
        Abril(:,2)=[];

        Maio=[];
        for i=1:length(dados)
            if dados(i,2)==5
               Maio = [Maio;dados(i,:)]; 
            end     
        end
        Maio(:,2)=[];

        Junho=[];
        for i=1:length(dados)  
            if dados(i,2)==6
               Junho = [Junho;dados(i,:)]; 
            end     
        end
        Junho(:,2)=[];

        Julho=[];
        for i=1:length(dados)
            if dados(i,2)==7
               Julho = [Julho;dados(i,:)]; 
            end     
        end
        Julho(:,2)=[];

        Agosto=[];
        for i=1:length(dados) 
            if dados(i,2)==8
               Agosto = [Agosto;dados(i,:)]; 
            end     
        end
        Agosto(:,2)=[]; 

        Setembro=[];
        for i=1:length(dados)  
            if dados(i,2)==9
               Setembro = [Setembro;dados(i,:)]; 
            end     
        end
        Setembro(:,2)=[];

        Outubro=[];
        for i=1:length(dados)  
            if dados(i,2)==10
               Outubro = [Outubro;dados(i,:)]; 
            end     
        end
        Outubro(:,2)=[];


        Novembro=[];
        for i=1:length(dados) 
            if dados(i,2)==11
               Novembro = [Novembro;dados(i,:)]; 
            end
        end
        Novembro(:,2)=[];

        Dezembro=[];
        for i=1:length(dados)  
            if dados(i,2)==12
               Dezembro = [Dezembro;dados(i,:)]; 
            end     
        end
        Dezembro(:,2)=[];
    
end

end