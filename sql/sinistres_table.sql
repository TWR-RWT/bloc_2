CREATE TABLE assurerplus.sinistres
(
    id_sinistre serial primary key,
    id_user integer NOT NULL,
    nom varchar(50) NOT NULL,
    prenom varchar(50) NOT NULL,
    telephone varchar(20) NOT NULL,
    email varchar(50) NOT NULL,
    date_sinistre date NOT NULL,
    adresse_sinistre varchar(100) NOT NULL,
    ville_sinistre varchar(50) NOT NULL,
    code_postal_sinistre varchar(20) NOT NULL,
    description varchar(100) NOT NULL,
    file_sinistre varchar(100),
    status varchar(50),
    commentaires varchar(100),
    foreign key (id_user) references assurerplus.accounts(user_id)
);