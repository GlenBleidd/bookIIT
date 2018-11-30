PGDMP         9    	        	    v            bookIIT    10.4    10.4 %                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                       false            !           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                       false            "           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                       false            #           1262    16698    bookIIT    DATABASE     �   CREATE DATABASE "bookIIT" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'English_United States.1252' LC_CTYPE = 'English_United States.1252';
    DROP DATABASE "bookIIT";
             postgres    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
             postgres    false            $           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                  postgres    false    3                        3079    12924    plpgsql 	   EXTENSION     ?   CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;
    DROP EXTENSION plpgsql;
                  false            %           0    0    EXTENSION plpgsql    COMMENT     @   COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';
                       false    1            \           1247    16779    locationtype    TYPE     T   CREATE TYPE public.locationtype AS ENUM (
    'Non-College Location',
    'Room'
);
    DROP TYPE public.locationtype;
       public       postgres    false    3            �            1259    16736    account    TABLE     �   CREATE TABLE public.account (
    acc_id integer NOT NULL,
    acc_type integer NOT NULL,
    username character varying NOT NULL,
    email character varying NOT NULL,
    password character varying NOT NULL
);
    DROP TABLE public.account;
       public         postgres    false    3            �            1259    16734    account_acc_id_seq    SEQUENCE     �   CREATE SEQUENCE public.account_acc_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.account_acc_id_seq;
       public       postgres    false    198    3            &           0    0    account_acc_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.account_acc_id_seq OWNED BY public.account.acc_id;
            public       postgres    false    197            �            1259    16705 	   admin_acc    TABLE     �   CREATE TABLE public.admin_acc (
    admin_id character varying(8) NOT NULL,
    fname character varying NOT NULL,
    lname character varying NOT NULL,
    college character varying NOT NULL,
    contact character varying NOT NULL
);
    DROP TABLE public.admin_acc;
       public         postgres    false    3            �            1259    16810 	   locations    TABLE     r   CREATE TABLE public.locations (
    location_id integer NOT NULL,
    location_name character varying NOT NULL
);
    DROP TABLE public.locations;
       public         postgres    false    3            �            1259    16823    room    TABLE     �   CREATE TABLE public.room (
    room_id integer NOT NULL,
    room_name character varying NOT NULL,
    college character varying
);
    DROP TABLE public.room;
       public         postgres    false    3            �            1259    16746    user_acc    TABLE     �   CREATE TABLE public.user_acc (
    user_id integer NOT NULL,
    fname character varying,
    lname character varying,
    contact character varying
);
    DROP TABLE public.user_acc;
       public         postgres    false    3            �            1259    16785    venue    TABLE     �   CREATE TABLE public.venue (
    venue_id integer NOT NULL,
    capacity character varying,
    rate integer,
    equipment character varying,
    venue_type public.locationtype
);
    DROP TABLE public.venue;
       public         postgres    false    3    604            �            1259    16783    venue_venue_id_seq    SEQUENCE     �   CREATE SEQUENCE public.venue_venue_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.venue_venue_id_seq;
       public       postgres    false    3    201            '           0    0    venue_venue_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.venue_venue_id_seq OWNED BY public.venue.venue_id;
            public       postgres    false    200            �
           2604    16739    account acc_id    DEFAULT     p   ALTER TABLE ONLY public.account ALTER COLUMN acc_id SET DEFAULT nextval('public.account_acc_id_seq'::regclass);
 =   ALTER TABLE public.account ALTER COLUMN acc_id DROP DEFAULT;
       public       postgres    false    197    198    198            �
           2604    16788    venue venue_id    DEFAULT     p   ALTER TABLE ONLY public.venue ALTER COLUMN venue_id SET DEFAULT nextval('public.venue_venue_id_seq'::regclass);
 =   ALTER TABLE public.venue ALTER COLUMN venue_id DROP DEFAULT;
       public       postgres    false    201    200    201                      0    16736    account 
   TABLE DATA               N   COPY public.account (acc_id, acc_type, username, email, password) FROM stdin;
    public       postgres    false    198   &                 0    16705 	   admin_acc 
   TABLE DATA               M   COPY public.admin_acc (admin_id, fname, lname, college, contact) FROM stdin;
    public       postgres    false    196   o&                 0    16810 	   locations 
   TABLE DATA               ?   COPY public.locations (location_id, location_name) FROM stdin;
    public       postgres    false    202   �&                 0    16823    room 
   TABLE DATA               ;   COPY public.room (room_id, room_name, college) FROM stdin;
    public       postgres    false    203   �&                 0    16746    user_acc 
   TABLE DATA               B   COPY public.user_acc (user_id, fname, lname, contact) FROM stdin;
    public       postgres    false    199   �&                 0    16785    venue 
   TABLE DATA               P   COPY public.venue (venue_id, capacity, rate, equipment, venue_type) FROM stdin;
    public       postgres    false    201   '       (           0    0    account_acc_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.account_acc_id_seq', 4, true);
            public       postgres    false    197            )           0    0    venue_venue_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.venue_venue_id_seq', 2, true);
            public       postgres    false    200            �
           2606    16744    account account_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_pkey PRIMARY KEY (acc_id);
 >   ALTER TABLE ONLY public.account DROP CONSTRAINT account_pkey;
       public         postgres    false    198            �
           2606    16729    admin_acc admin_acc_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.admin_acc
    ADD CONSTRAINT admin_acc_pkey PRIMARY KEY (admin_id);
 B   ALTER TABLE ONLY public.admin_acc DROP CONSTRAINT admin_acc_pkey;
       public         postgres    false    196            �
           2606    16817    locations locations_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations_pkey PRIMARY KEY (location_id);
 B   ALTER TABLE ONLY public.locations DROP CONSTRAINT locations_pkey;
       public         postgres    false    202            �
           2606    16830    room room_pkey 
   CONSTRAINT     Q   ALTER TABLE ONLY public.room
    ADD CONSTRAINT room_pkey PRIMARY KEY (room_id);
 8   ALTER TABLE ONLY public.room DROP CONSTRAINT room_pkey;
       public         postgres    false    203            �
           2606    16753    user_acc user_acc_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.user_acc
    ADD CONSTRAINT user_acc_pkey PRIMARY KEY (user_id);
 @   ALTER TABLE ONLY public.user_acc DROP CONSTRAINT user_acc_pkey;
       public         postgres    false    199            �
           2606    16793    venue venue_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.venue
    ADD CONSTRAINT venue_pkey PRIMARY KEY (venue_id);
 :   ALTER TABLE ONLY public.venue DROP CONSTRAINT venue_pkey;
       public         postgres    false    201            �
           2606    16818 $   locations locations_location_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations_location_id_fkey FOREIGN KEY (location_id) REFERENCES public.venue(venue_id);
 N   ALTER TABLE ONLY public.locations DROP CONSTRAINT locations_location_id_fkey;
       public       postgres    false    201    2710    202            �
           2606    16831    room room_room_id_fkey    FK CONSTRAINT     {   ALTER TABLE ONLY public.room
    ADD CONSTRAINT room_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.venue(venue_id);
 @   ALTER TABLE ONLY public.room DROP CONSTRAINT room_room_id_fkey;
       public       postgres    false    2710    201    203               D   x�3�4��M,�����`R/9?��2�{�g�9��%rf�@�Cyy*XMFfq^bnjf1W� �=�            x������ � �         !   x�3�����Qp���K,�,������ [��            x�3����U06��v����� 2�7            x�3������tN�K������ ,         X   x�3�45 "΀������"Π��\.#N#��!�T���ofrQ~AF~^*�\����ZT�闟�뜟���������X�������� Hk8     