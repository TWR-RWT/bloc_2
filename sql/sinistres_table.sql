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
    description varchar(100) NOT NULL,
    file_sinistre varchar(100) NOT NULL,
    foreign key (id_user) references assurerplus.accounts(user_id)
);