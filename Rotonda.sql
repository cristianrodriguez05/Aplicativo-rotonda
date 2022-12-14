-- Generated by Oracle SQL Developer Data Modeler 22.2.0.165.1149
--   at:        2022-12-14 20:41:23 COT
--   site:      Oracle Database 11g
--   type:      Oracle Database 11g



-- predefined type, no DDL - MDSYS.SDO_GEOMETRY

-- predefined type, no DDL - XMLTYPE

CREATE TABLE carrito_compra (
    valor_carrito   NUMBER,
    usuario_carrito NUMBER NOT NULL
);

CREATE UNIQUE INDEX carrito_compra__idx ON
    carrito_compra (
        usuario_carrito
    ASC );

ALTER TABLE carrito_compra ADD CONSTRAINT carrito_compra_pk PRIMARY KEY ( usuario_carrito );

CREATE TABLE ingrediente (
    id_ingrediente          VARCHAR2(25) NOT NULL,
    precio_ingrediente      NUMBER NOT NULL,
    restaurante_ingrediente VARCHAR2(10) NOT NULL
);

ALTER TABLE ingrediente ADD CONSTRAINT ingrediente_pk PRIMARY KEY ( id_ingrediente );

CREATE TABLE menu (
    id_menu          VARCHAR2(10) NOT NULL,
    nombre_menu      VARCHAR2(25) NOT NULL,
    precio_menu      NUMBER NOT NULL,
    restaurante_menu VARCHAR2(10) NOT NULL
);

ALTER TABLE menu ADD CONSTRAINT menu_pk PRIMARY KEY ( id_menu );

CREATE TABLE pedido (
    id_pedido      VARCHAR2(10) NOT NULL,
    costo_pedido   NUMBER NOT NULL,
    usuario_pedido NUMBER NOT NULL
);

ALTER TABLE pedido ADD CONSTRAINT pedido_pk PRIMARY KEY ( id_pedido );

CREATE TABLE producto (
    id_producto          VARCHAR2(25) NOT NULL,
    precio_producto      NUMBER NOT NULL,
    tipo_producto        VARCHAR2(20) NOT NULL,
    restaurante_producto VARCHAR2(10) NOT NULL
);

ALTER TABLE producto ADD CONSTRAINT producto_pk PRIMARY KEY ( id_producto );

CREATE TABLE restaurante (
    id_restaurante VARCHAR2(10) NOT NULL,
    nombre_rest    VARCHAR2(30) NOT NULL,
    especialidad   VARCHAR2(20) NOT NULL,
    correo         VARCHAR2(30) NOT NULL
);

ALTER TABLE restaurante ADD CONSTRAINT restaurante_pk PRIMARY KEY ( id_restaurante );

CREATE TABLE rompimiento (
    numero_pedido       VARCHAR2(10) NOT NULL,
    menu_elegido        VARCHAR2(10),
    producto_elegido    VARCHAR2(25),
    ingrediente_elegido VARCHAR2(25),
    precio              NUMBER
);

ALTER TABLE rompimiento ADD CONSTRAINT rompimiento_pk PRIMARY KEY ( numero_pedido );

CREATE TABLE usuario (
    id_usuario NUMBER NOT NULL,
    nombre     VARCHAR2(20 CHAR) NOT NULL,
    apellido   VARCHAR2(20 CHAR) NOT NULL,
    correo     VARCHAR2(40 CHAR) NOT NULL,
    contrase?a VARCHAR2(25 CHAR) NOT NULL,
    direccion  VARCHAR2(40) NOT NULL
);

ALTER TABLE usuario ADD CONSTRAINT usuario_pk PRIMARY KEY ( id_usuario );

ALTER TABLE carrito_compra
    ADD CONSTRAINT carrito_compra_usuario_fk FOREIGN KEY ( usuario_carrito )
        REFERENCES usuario ( id_usuario );

ALTER TABLE ingrediente
    ADD CONSTRAINT ingrediente_restaurante_fk FOREIGN KEY ( restaurante_ingrediente )
        REFERENCES restaurante ( id_restaurante );

ALTER TABLE menu
    ADD CONSTRAINT menu_restaurante_fk FOREIGN KEY ( restaurante_menu )
        REFERENCES restaurante ( id_restaurante );

ALTER TABLE pedido
    ADD CONSTRAINT pedido_carrito_compra_fk FOREIGN KEY ( usuario_pedido )
        REFERENCES carrito_compra ( usuario_carrito );

ALTER TABLE producto
    ADD CONSTRAINT producto_restaurante_fk FOREIGN KEY ( restaurante_producto )
        REFERENCES restaurante ( id_restaurante );

ALTER TABLE rompimiento
    ADD CONSTRAINT rompimiento_ingrediente_fk FOREIGN KEY ( ingrediente_elegido )
        REFERENCES ingrediente ( id_ingrediente );

ALTER TABLE rompimiento
    ADD CONSTRAINT rompimiento_menu_fk FOREIGN KEY ( menu_elegido )
        REFERENCES menu ( id_menu );

ALTER TABLE rompimiento
    ADD CONSTRAINT rompimiento_pedido_fk FOREIGN KEY ( numero_pedido )
        REFERENCES pedido ( id_pedido );

ALTER TABLE rompimiento
    ADD CONSTRAINT rompimiento_producto_fk FOREIGN KEY ( producto_elegido )
        REFERENCES producto ( id_producto );



-- Oracle SQL Developer Data Modeler Summary Report: 
-- 
-- CREATE TABLE                             8
-- CREATE INDEX                             1
-- ALTER TABLE                             17
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           0
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          0
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   0