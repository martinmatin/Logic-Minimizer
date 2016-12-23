function Issame = IsSameFunction(A,B,nbrvar)

%Entrées: matrice A, matrice B et nombre de variable nbrvar
%Sortie: Issame (1 si A et B sont les mêmes fonctions, 0 si elles sont différentes)

%Exemple: A et B sont des matrices contenant des cubes
%
%nbrvar = 6;
%test = IsSameFunction(A,B,nbrvar)
%

%Parcourir tous les cubes et les mettre dans la table de vérité pour A
valtotA = [];
for a=1:1:size(A,1) %parcourir les cubes
  cube = A(a,:); %un cube
  val = [0];
    for c=1:1:size(cube,2)%parcourir les variables
      poids = 2^(nbrvar-c);
      if (cube(c)==1) %ajouter le poids pour un index
      val= val + poids;
      else if (cube(c)==3)     %couper en deux et ajouter le poids pour un index
            val2 = val + poids;
            val = [val;val2];
          end
      end      
    end
  valtotA= [valtotA;val];
end
valtotA=sort(valtotA);
valtotA1= [valtotA;0];
valtotA2= [0;valtotA];
ind=find(valtotA1~=valtotA2);
ind=ind(1:size(ind)-1);
valtotA=valtotA(ind);

%Parcourir tous les cubes et les mettre dans la table de vérité pour B
valtotB = [];
for a=1:1:size(B,1) %parcourir les cubes
  cube = B(a,:); %un cube
  val = [0];
    for c=1:1:size(cube,2)%parcourir les variables
      poids = 2^(nbrvar-c);
      if (cube(c)==1) %ajouter le poids pour un index
      val= val + poids;
      else if (cube(c)==3)     %couper en deux et ajouter le poids pour un index
            val2 = val + poids;
            val = [val;val2];
          end
      end      
    end
  valtotB= [valtotB;val];
end
valtotB=sort(valtotB);
valtotB1= [valtotB;0];
valtotB2= [0;valtotB];
ind=find(valtotB1~=valtotB2);
ind=ind(1:size(ind)-1);
valtotB=valtotB(ind);

Issame=0;

if (length(valtotB)==length(valtotA))
   Issame =all(valtotB==valtotA);
end

return