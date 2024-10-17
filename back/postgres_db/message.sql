-- Table: level
CREATE TABLE level (
    id SERIAL PRIMARY KEY,  -- id auto-incrémenté
    name VARCHAR(255) NOT NULL,  -- nom du niveau, non nul
    testimonies_needed INTEGER  -- nombre de témoignages nécessaires
);

-- Table: target
CREATE TABLE target (
    id SERIAL PRIMARY KEY,  -- id auto-incrémenté
    name VARCHAR(255) NOT NULL  -- nom de la cible, non nul
);

-- Table: harassment
CREATE TABLE harassment_type (
    id SERIAL PRIMARY KEY,  -- id auto-incrémenté
    name VARCHAR(255) NOT NULL  -- nom de la cible, non nul
);

CREATE TABLE platform (
    id SERIAL PRIMARY KEY,  -- id auto-incrémenté
    name VARCHAR(255) NOT NULL,  -- nom de la cible, non nul
    image VARCHAR(255)
);

-- Table: message
CREATE TABLE message (
    id SERIAL PRIMARY KEY,  -- id auto-incrémenté
    description TEXT,  -- description du message
    level_id INTEGER,  -- référence à la table level
    stalker_id INTEGER,  -- référence à la table target
    harassment_type_id INTEGER,
    platform_id INTEGER,
    FOREIGN KEY (level_id) REFERENCES level(id),  -- clé étrangère vers level
    FOREIGN KEY (stalker_id) REFERENCES target(id),  -- clé étrangère vers target
    FOREIGN KEY (harassment_type_id) REFERENCES harassment_type(id),
    FOREIGN KEY (platform_id) REFERENCES platform(id)  -- clé étrangère vers platform
);