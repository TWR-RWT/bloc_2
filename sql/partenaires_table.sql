CREATE TABLE assurerplus.partenaires
(
    id serial primary key,
    type_ varchar(50) NOT NULL,
    entreprise varchar(50) NOT NULL,
    telephone varchar(20) NOT NULL,
    email varchar(50),
    adresse varchar(100) NOT NULL,
    ville varchar(50) NOT NULL,
    code_postal varchar(20) NOT NULL,
    website varchar(100),
);