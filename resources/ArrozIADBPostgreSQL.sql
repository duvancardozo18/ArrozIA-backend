PGDMP  6    (            
    |         
   ArrozIA_33    16.3    16.3 �   �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    65560 
   ArrozIA_33    DATABASE     �   CREATE DATABASE "ArrozIA_33" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Mexico.1252';
    DROP DATABASE "ArrozIA_33";
                postgres    false            4           1255    65561    generate_slug(text)    FUNCTION       CREATE FUNCTION public.generate_slug(name text) RETURNS text
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Convertimos el nombre a minúsculas, reemplazamos espacios por guiones y eliminamos caracteres especiales
    RETURN LOWER(REGEXP_REPLACE(name, '[^a-zA-Z0-9]+', '-', 'g'));
END;
$$;
 /   DROP FUNCTION public.generate_slug(name text);
       public          postgres    false            5           1255    65562    set_slug_cultivo()    FUNCTION     �   CREATE FUNCTION public.set_slug_cultivo() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.slug := generate_slug(NEW.nombre_cultivo); -- Correct field reference
    RETURN NEW;
END;
$$;
 )   DROP FUNCTION public.set_slug_cultivo();
       public          postgres    false            6           1255    65563    set_slug_finca()    FUNCTION     �   CREATE FUNCTION public.set_slug_finca() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.slug := generate_slug(NEW.nombre);
    RETURN NEW;
END;
$$;
 '   DROP FUNCTION public.set_slug_finca();
       public          postgres    false            7           1255    65564    set_slug_lote()    FUNCTION     �   CREATE FUNCTION public.set_slug_lote() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.slug := generate_slug(NEW.nombre);
    RETURN NEW;
END;
$$;
 &   DROP FUNCTION public.set_slug_lote();
       public          postgres    false            8           1255    65565    update_actualizado_en()    FUNCTION     �   CREATE FUNCTION public.update_actualizado_en() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.actualizado_en = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;
 .   DROP FUNCTION public.update_actualizado_en();
       public          postgres    false            9           1255    65566    update_timestamp()    FUNCTION     �   CREATE FUNCTION public.update_timestamp() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.actualizado_en = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;
 )   DROP FUNCTION public.update_timestamp();
       public          postgres    false            �            1259    65567    agua    TABLE     F  CREATE TABLE public.agua (
    id integer NOT NULL,
    costo_instalacion_agua_real numeric(10,2),
    costo_instalacion_agua_estimado numeric(10,2),
    costo_consumo_agua_real numeric(10,2),
    costo_consumo_agua_estimado numeric(10,2),
    consumo_energia_real numeric(10,2),
    consumo_energia_estimada numeric(10,2)
);
    DROP TABLE public.agua;
       public         heap    postgres    false            �            1259    65570    agua_id_seq    SEQUENCE     �   CREATE SEQUENCE public.agua_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE public.agua_id_seq;
       public          postgres    false    215            �           0    0    agua_id_seq    SEQUENCE OWNED BY     ;   ALTER SEQUENCE public.agua_id_seq OWNED BY public.agua.id;
          public          postgres    false    216            �            1259    65571    analisis_edafologico    TABLE     T  CREATE TABLE public.analisis_edafologico (
    id integer NOT NULL,
    lote_id integer NOT NULL,
    fecha_analisis date NOT NULL,
    tipo_suelo_id integer NOT NULL,
    archivo_reporte bytea,
    creado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    actualizado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
 (   DROP TABLE public.analisis_edafologico;
       public         heap    postgres    false            �            1259    65578    analisis_edafologico_id_seq    SEQUENCE     �   CREATE SEQUENCE public.analisis_edafologico_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 2   DROP SEQUENCE public.analisis_edafologico_id_seq;
       public          postgres    false    217            �           0    0    analisis_edafologico_id_seq    SEQUENCE OWNED BY     [   ALTER SEQUENCE public.analisis_edafologico_id_seq OWNED BY public.analisis_edafologico.id;
          public          postgres    false    218            3           1259    66205 
   audit_logs    TABLE       CREATE TABLE public.audit_logs (
    id integer NOT NULL,
    table_name character varying NOT NULL,
    operation_type character varying NOT NULL,
    record_id integer NOT NULL,
    changed_data json,
    operation_timestamp timestamp without time zone NOT NULL
);
    DROP TABLE public.audit_logs;
       public         heap    postgres    false            2           1259    66204    audit_logs_id_seq    SEQUENCE     �   CREATE SEQUENCE public.audit_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.audit_logs_id_seq;
       public          postgres    false    307            �           0    0    audit_logs_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.audit_logs_id_seq OWNED BY public.audit_logs.id;
          public          postgres    false    306            �            1259    65579    color    TABLE     h   CREATE TABLE public.color (
    id integer NOT NULL,
    descripcion character varying(255) NOT NULL
);
    DROP TABLE public.color;
       public         heap    postgres    false            �            1259    65582    color_id_seq    SEQUENCE     �   CREATE SEQUENCE public.color_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.color_id_seq;
       public          postgres    false    219            �           0    0    color_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.color_id_seq OWNED BY public.color.id;
          public          postgres    false    220            �            1259    65583    cosecha    TABLE     �  CREATE TABLE public.cosecha (
    id integer NOT NULL,
    cultivo_id integer NOT NULL,
    fecha_estimada_cosecha date,
    fecha_cosecha date,
    precio_carga_mercado double precision NOT NULL,
    gasto_transporte_cosecha double precision NOT NULL,
    gasto_recoleccion double precision NOT NULL,
    cantidad_producida_cosecha double precision NOT NULL,
    venta_cosecha double precision NOT NULL
);
    DROP TABLE public.cosecha;
       public         heap    postgres    false            �            1259    65586    cosecha_id_seq    SEQUENCE     �   CREATE SEQUENCE public.cosecha_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.cosecha_id_seq;
       public          postgres    false    221            �           0    0    cosecha_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.cosecha_id_seq OWNED BY public.cosecha.id;
          public          postgres    false    222            �            1259    65587    costos_adicionales    TABLE        CREATE TABLE public.costos_adicionales (
    id integer NOT NULL,
    costo_capacitacion_real numeric(10,2),
    costo_capacitacion_estimado numeric(10,2),
    costo_control_roedores_real numeric(10,2),
    costo_control_roedores_estimado numeric(10,2)
);
 &   DROP TABLE public.costos_adicionales;
       public         heap    postgres    false            �            1259    65590    costos_adicionales_id_seq    SEQUENCE     �   CREATE SEQUENCE public.costos_adicionales_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.costos_adicionales_id_seq;
       public          postgres    false    223            �           0    0    costos_adicionales_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.costos_adicionales_id_seq OWNED BY public.costos_adicionales.id;
          public          postgres    false    224            �            1259    65591    costos_estimados    TABLE     �  CREATE TABLE public.costos_estimados (
    id integer NOT NULL,
    cantidad_insumo double precision NOT NULL,
    costo_insumo double precision NOT NULL,
    horas_de_uso_de_maquinaria double precision NOT NULL,
    costo_maquinaria double precision NOT NULL,
    numero_trabajadores_por_dia integer NOT NULL,
    numero_dias_trabajados integer NOT NULL,
    costo_mano_obra double precision NOT NULL,
    tarea_labor_id integer NOT NULL
);
 $   DROP TABLE public.costos_estimados;
       public         heap    postgres    false            �            1259    65594    costos_estimados_id_seq    SEQUENCE     �   CREATE SEQUENCE public.costos_estimados_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.costos_estimados_id_seq;
       public          postgres    false    225            �           0    0    costos_estimados_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.costos_estimados_id_seq OWNED BY public.costos_estimados.id;
          public          postgres    false    226            �            1259    65595    costos_reales    TABLE     �  CREATE TABLE public.costos_reales (
    id integer NOT NULL,
    cantidad_insumo double precision NOT NULL,
    costo_insumo double precision NOT NULL,
    horas_de_uso_de_maquinaria double precision NOT NULL,
    costo_maquinaria double precision NOT NULL,
    numero_trabajadores_por_dia integer NOT NULL,
    numero_dias_trabajados integer NOT NULL,
    costo_mano_obra double precision NOT NULL,
    tarea_labor_id integer NOT NULL
);
 !   DROP TABLE public.costos_reales;
       public         heap    postgres    false            �            1259    65598    costos_reales_id_seq    SEQUENCE     �   CREATE SEQUENCE public.costos_reales_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.costos_reales_id_seq;
       public          postgres    false    227            �           0    0    costos_reales_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.costos_reales_id_seq OWNED BY public.costos_reales.id;
          public          postgres    false    228            �            1259    65599    cultivo    TABLE       CREATE TABLE public.cultivo (
    id integer NOT NULL,
    nombre_cultivo character varying(50) NOT NULL,
    variedad_id integer NOT NULL,
    lote_id integer NOT NULL,
    fecha_siembra date NOT NULL,
    fecha_estimada_cosecha date NOT NULL,
    slug character varying(255)
);
    DROP TABLE public.cultivo;
       public         heap    postgres    false            �            1259    65602    cultivo_id_seq    SEQUENCE     �   CREATE SEQUENCE public.cultivo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.cultivo_id_seq;
       public          postgres    false    229            �           0    0    cultivo_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.cultivo_id_seq OWNED BY public.cultivo.id;
          public          postgres    false    230            �            1259    65609    diagnostico_fitosanitario    TABLE     �  CREATE TABLE public.diagnostico_fitosanitario (
    id integer NOT NULL,
    resultado_ia json,
    ruta character varying(255),
    cultivo_id integer,
    fecha_diagnostico timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    confianza_promedio numeric(5,2),
    tipo_problema character varying(50),
    imagenes_analizadas json,
    exportado boolean DEFAULT false,
    comparacion_diagnostico json
);
 -   DROP TABLE public.diagnostico_fitosanitario;
       public         heap    postgres    false            �            1259    65616     diagnostico_fitosanitario_id_seq    SEQUENCE     �   CREATE SEQUENCE public.diagnostico_fitosanitario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 7   DROP SEQUENCE public.diagnostico_fitosanitario_id_seq;
       public          postgres    false    231            �           0    0     diagnostico_fitosanitario_id_seq    SEQUENCE OWNED BY     e   ALTER SEQUENCE public.diagnostico_fitosanitario_id_seq OWNED BY public.diagnostico_fitosanitario.id;
          public          postgres    false    232            �            1259    65617    estado    TABLE     z   CREATE TABLE public.estado (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion text
);
    DROP TABLE public.estado;
       public         heap    postgres    false            �            1259    65622    estado_id_seq    SEQUENCE     �   CREATE SEQUENCE public.estado_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.estado_id_seq;
       public          postgres    false    233            �           0    0    estado_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.estado_id_seq OWNED BY public.estado.id;
          public          postgres    false    234            �            1259    65623    etapa_fenologica    TABLE     �   CREATE TABLE public.etapa_fenologica (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    fase character varying(50) NOT NULL
);
 $   DROP TABLE public.etapa_fenologica;
       public         heap    postgres    false            �            1259    65626    etapa_fenologica_id_seq    SEQUENCE     �   CREATE SEQUENCE public.etapa_fenologica_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.etapa_fenologica_id_seq;
       public          postgres    false    235            �           0    0    etapa_fenologica_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.etapa_fenologica_id_seq OWNED BY public.etapa_fenologica.id;
          public          postgres    false    236            �            1259    65627    finca    TABLE     n  CREATE TABLE public.finca (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL,
    ubicacion character varying(100),
    area_total double precision,
    latitud numeric(10,5),
    longitud numeric(10,5),
    slug character varying(255),
    ciudad character varying(100),
    departamento character varying(100),
    pais character varying(100)
);
    DROP TABLE public.finca;
       public         heap    postgres    false            �            1259    65632    finca_id_seq    SEQUENCE     �   CREATE SEQUENCE public.finca_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.finca_id_seq;
       public          postgres    false    237            �           0    0    finca_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.finca_id_seq OWNED BY public.finca.id;
          public          postgres    false    238            �            1259    65633    gastos    TABLE     �   CREATE TABLE public.gastos (
    id integer NOT NULL,
    cultivo_id integer NOT NULL,
    concepto character varying(255) NOT NULL,
    descripcion text,
    precio double precision NOT NULL
);
    DROP TABLE public.gastos;
       public         heap    postgres    false            �            1259    65638 "   gastos_administrativos_financieros    TABLE     �   CREATE TABLE public.gastos_administrativos_financieros (
    id integer NOT NULL,
    costo_impuestos_real numeric(10,2),
    costo_impuestos_estimado numeric(10,2),
    costo_seguros_real numeric(10,2),
    costo_seguros_estimado numeric(10,2)
);
 6   DROP TABLE public.gastos_administrativos_financieros;
       public         heap    postgres    false            �            1259    65641 )   gastos_administrativos_financieros_id_seq    SEQUENCE     �   CREATE SEQUENCE public.gastos_administrativos_financieros_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 @   DROP SEQUENCE public.gastos_administrativos_financieros_id_seq;
       public          postgres    false    240            �           0    0 )   gastos_administrativos_financieros_id_seq    SEQUENCE OWNED BY     w   ALTER SEQUENCE public.gastos_administrativos_financieros_id_seq OWNED BY public.gastos_administrativos_financieros.id;
          public          postgres    false    241            �            1259    65642    gastos_id_seq    SEQUENCE     �   CREATE SEQUENCE public.gastos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.gastos_id_seq;
       public          postgres    false    239            �           0    0    gastos_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.gastos_id_seq OWNED BY public.gastos.id;
          public          postgres    false    242            �            1259    65643    gastos_variables    TABLE     �   CREATE TABLE public.gastos_variables (
    id integer NOT NULL,
    id_costos_adicionales integer,
    id_agua integer,
    id_gastos_administrativos_financieros integer,
    descripcion text
);
 $   DROP TABLE public.gastos_variables;
       public         heap    postgres    false            �            1259    65648    gastos_variables_id_seq    SEQUENCE     �   CREATE SEQUENCE public.gastos_variables_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.gastos_variables_id_seq;
       public          postgres    false    243            �           0    0    gastos_variables_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.gastos_variables_id_seq OWNED BY public.gastos_variables.id;
          public          postgres    false    244            �            1259    65649    insumo_agricola    TABLE     v  CREATE TABLE public.insumo_agricola (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion text,
    costo_unitario double precision NOT NULL,
    cantidad numeric(10,2) DEFAULT 0,
    unidad_id integer,
    precio_unitario_estimado numeric(10,2),
    cultivo_id integer,
    cantidad_estimada double precision,
    tipo_insumo_id integer
);
 #   DROP TABLE public.insumo_agricola;
       public         heap    postgres    false            �            1259    65655    insumo_agricola_id_seq    SEQUENCE     �   CREATE SEQUENCE public.insumo_agricola_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.insumo_agricola_id_seq;
       public          postgres    false    245            �           0    0    insumo_agricola_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.insumo_agricola_id_seq OWNED BY public.insumo_agricola.id;
          public          postgres    false    246            �            1259    65656    labor_cultural    TABLE     �   CREATE TABLE public.labor_cultural (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion text,
    precio_hectaria numeric(10,2),
    precio_hectaria_estimada numeric(10,2),
    id_etapa_fenologica integer
);
 "   DROP TABLE public.labor_cultural;
       public         heap    postgres    false            �            1259    65661    labor_cultural_id_seq    SEQUENCE     �   CREATE SEQUENCE public.labor_cultural_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.labor_cultural_id_seq;
       public          postgres    false    247            �           0    0    labor_cultural_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.labor_cultural_id_seq OWNED BY public.labor_cultural.id;
          public          postgres    false    248            �            1259    65662    lote    TABLE     p  CREATE TABLE public.lote (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    finca_id integer NOT NULL,
    area double precision NOT NULL,
    latitud numeric(10,5),
    longitud numeric(10,5),
    slug character varying(255),
    costo_arriendo_real numeric(10,2),
    costo_arriendo_estimado numeric(10,2),
    arriendo_real numeric(10,2)
);
    DROP TABLE public.lote;
       public         heap    postgres    false            �            1259    65665    lote_id_seq    SEQUENCE     �   CREATE SEQUENCE public.lote_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE public.lote_id_seq;
       public          postgres    false    249            �           0    0    lote_id_seq    SEQUENCE OWNED BY     ;   ALTER SEQUENCE public.lote_id_seq OWNED BY public.lote.id;
          public          postgres    false    250            �            1259    65666    macronutriente    TABLE     !  CREATE TABLE public.macronutriente (
    id integer NOT NULL,
    parametro_quimico_id integer NOT NULL,
    n numeric(10,2) NOT NULL,
    p numeric(10,2) NOT NULL,
    k numeric(10,2) NOT NULL,
    ca numeric(10,2) NOT NULL,
    mg numeric(10,2) NOT NULL,
    s numeric(10,2) NOT NULL
);
 "   DROP TABLE public.macronutriente;
       public         heap    postgres    false            �            1259    65669    macronutriente_id_seq    SEQUENCE     �   CREATE SEQUENCE public.macronutriente_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.macronutriente_id_seq;
       public          postgres    false    251            �           0    0    macronutriente_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.macronutriente_id_seq OWNED BY public.macronutriente.id;
          public          postgres    false    252            �            1259    65670 	   mano_obra    TABLE     �   CREATE TABLE public.mano_obra (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion text,
    costo_dia double precision NOT NULL
);
    DROP TABLE public.mano_obra;
       public         heap    postgres    false            �            1259    65675    mano_obra_id_seq    SEQUENCE     �   CREATE SEQUENCE public.mano_obra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.mano_obra_id_seq;
       public          postgres    false    253            �           0    0    mano_obra_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.mano_obra_id_seq OWNED BY public.mano_obra.id;
          public          postgres    false    254            �            1259    65676    maquinaria_agricola    TABLE     �   CREATE TABLE public.maquinaria_agricola (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion text,
    costo_hora double precision NOT NULL,
    costo_hora_estimado double precision
);
 '   DROP TABLE public.maquinaria_agricola;
       public         heap    postgres    false                        1259    65681    maquinaria_agricola_id_seq    SEQUENCE     �   CREATE SEQUENCE public.maquinaria_agricola_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.maquinaria_agricola_id_seq;
       public          postgres    false    255            �           0    0    maquinaria_agricola_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.maquinaria_agricola_id_seq OWNED BY public.maquinaria_agricola.id;
          public          postgres    false    256                       1259    65682    micronutriente    TABLE     �   CREATE TABLE public.micronutriente (
    id integer NOT NULL,
    parametro_quimico_id integer NOT NULL,
    fe numeric(10,2),
    cu numeric(10,2),
    mn numeric(10,2),
    zn numeric(10,2),
    b numeric(10,2)
);
 "   DROP TABLE public.micronutriente;
       public         heap    postgres    false                       1259    65685    micronutriente_id_seq    SEQUENCE     �   CREATE SEQUENCE public.micronutriente_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.micronutriente_id_seq;
       public          postgres    false    257            �           0    0    micronutriente_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.micronutriente_id_seq OWNED BY public.micronutriente.id;
          public          postgres    false    258                       1259    65686 
   monitoreos    TABLE       CREATE TABLE public.monitoreos (
    id integer NOT NULL,
    tipo character varying(100) NOT NULL,
    variedad_arroz_etapa_fenologica_id integer,
    recomendacion text,
    crop_id integer,
    fecha_programada date,
    fecha_finalizacion date,
    estado character(1)
);
    DROP TABLE public.monitoreos;
       public         heap    postgres    false                       1259    65691    monitoreos_id_seq    SEQUENCE     �   CREATE SEQUENCE public.monitoreos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.monitoreos_id_seq;
       public          postgres    false    259            �           0    0    monitoreos_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.monitoreos_id_seq OWNED BY public.monitoreos.id;
          public          postgres    false    260                       1259    65692    operacion_mecanizacion    TABLE     �   CREATE TABLE public.operacion_mecanizacion (
    id integer NOT NULL,
    tarea_labor_id integer NOT NULL,
    nombre_mecanizacion character varying(50) NOT NULL,
    maquinaria_id integer NOT NULL,
    horas_uso numeric(5,2) NOT NULL
);
 *   DROP TABLE public.operacion_mecanizacion;
       public         heap    postgres    false                       1259    65695    operacion_mecanizacion_id_seq    SEQUENCE     �   CREATE SEQUENCE public.operacion_mecanizacion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.operacion_mecanizacion_id_seq;
       public          postgres    false    261            �           0    0    operacion_mecanizacion_id_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.operacion_mecanizacion_id_seq OWNED BY public.operacion_mecanizacion.id;
          public          postgres    false    262                       1259    65696    parametro_biologico    TABLE     �   CREATE TABLE public.parametro_biologico (
    id integer NOT NULL,
    analisis_edafologico_id integer NOT NULL,
    biomasa_microbiana numeric(10,2),
    actividad_enzimatica numeric(10,2)
);
 '   DROP TABLE public.parametro_biologico;
       public         heap    postgres    false                       1259    65699    parametro_biologico_id_seq    SEQUENCE     �   CREATE SEQUENCE public.parametro_biologico_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.parametro_biologico_id_seq;
       public          postgres    false    263            �           0    0    parametro_biologico_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.parametro_biologico_id_seq OWNED BY public.parametro_biologico.id;
          public          postgres    false    264            	           1259    65700    parametro_fisico    TABLE     �   CREATE TABLE public.parametro_fisico (
    id integer NOT NULL,
    analisis_edafologico_id integer NOT NULL,
    textura_id integer NOT NULL,
    densidad_aparente numeric(10,2),
    profundidad_efectiva numeric(10,2),
    color_id integer NOT NULL
);
 $   DROP TABLE public.parametro_fisico;
       public         heap    postgres    false            
           1259    65703    parametro_fisico_id_seq    SEQUENCE     �   CREATE SEQUENCE public.parametro_fisico_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.parametro_fisico_id_seq;
       public          postgres    false    265            �           0    0    parametro_fisico_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.parametro_fisico_id_seq OWNED BY public.parametro_fisico.id;
          public          postgres    false    266                       1259    65704    parametro_quimico    TABLE       CREATE TABLE public.parametro_quimico (
    id integer NOT NULL,
    analisis_edafologico_id integer NOT NULL,
    ph numeric(4,2) NOT NULL,
    conductividad_electrica numeric(10,2),
    materia_organica numeric(10,2) NOT NULL,
    capacidad_intercambio_cationico numeric(10,2)
);
 %   DROP TABLE public.parametro_quimico;
       public         heap    postgres    false                       1259    65707    parametro_quimico_id_seq    SEQUENCE     �   CREATE SEQUENCE public.parametro_quimico_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.parametro_quimico_id_seq;
       public          postgres    false    267            �           0    0    parametro_quimico_id_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.parametro_quimico_id_seq OWNED BY public.parametro_quimico.id;
          public          postgres    false    268                       1259    65708    password_resets    TABLE     �   CREATE TABLE public.password_resets (
    id integer NOT NULL,
    email character varying NOT NULL,
    token character varying NOT NULL,
    created_at timestamp without time zone
);
 #   DROP TABLE public.password_resets;
       public         heap    postgres    false                       1259    65713    password_resets_id_seq    SEQUENCE     �   CREATE SEQUENCE public.password_resets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.password_resets_id_seq;
       public          postgres    false    269            �           0    0    password_resets_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.password_resets_id_seq OWNED BY public.password_resets.id;
          public          postgres    false    270                       1259    65714    permiso    TABLE     {   CREATE TABLE public.permiso (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion text
);
    DROP TABLE public.permiso;
       public         heap    postgres    false                       1259    65719    permiso_id_seq    SEQUENCE     �   CREATE SEQUENCE public.permiso_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.permiso_id_seq;
       public          postgres    false    271            �           0    0    permiso_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.permiso_id_seq OWNED BY public.permiso.id;
          public          postgres    false    272                       1259    65720    phenological_stages    TABLE     �   CREATE TABLE public.phenological_stages (
    id integer NOT NULL,
    rice_variety_id integer NOT NULL,
    stage_name character varying(100) NOT NULL,
    duration_days integer NOT NULL
);
 '   DROP TABLE public.phenological_stages;
       public         heap    postgres    false                       1259    65723    phenological_stages_id_seq    SEQUENCE     �   CREATE SEQUENCE public.phenological_stages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.phenological_stages_id_seq;
       public          postgres    false    273            �           0    0    phenological_stages_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.phenological_stages_id_seq OWNED BY public.phenological_stages.id;
          public          postgres    false    274                       1259    65724    registro_meteorologico    TABLE       CREATE TABLE public.registro_meteorologico (
    id integer NOT NULL,
    lote_id integer NOT NULL,
    fecha date NOT NULL,
    temperatura numeric(5,2) NOT NULL,
    presion_atmosferica numeric(6,2) NOT NULL,
    humedad numeric(5,2) NOT NULL,
    precipitacion numeric(5,2),
    indice_ultravioleta numeric(4,2) NOT NULL,
    horas_sol numeric(4,2) NOT NULL,
    fuente_datos character varying(50),
    hora time without time zone,
    api_respuesta json,
    creado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
 *   DROP TABLE public.registro_meteorologico;
       public         heap    postgres    false                       1259    65730    registro_meteorologico_id_seq    SEQUENCE     �   CREATE SEQUENCE public.registro_meteorologico_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.registro_meteorologico_id_seq;
       public          postgres    false    275            �           0    0    registro_meteorologico_id_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.registro_meteorologico_id_seq OWNED BY public.registro_meteorologico.id;
          public          postgres    false    276                       1259    65731    rice_varieties    TABLE     j   CREATE TABLE public.rice_varieties (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);
 "   DROP TABLE public.rice_varieties;
       public         heap    postgres    false                       1259    65734    rice_varieties_id_seq    SEQUENCE     �   CREATE SEQUENCE public.rice_varieties_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.rice_varieties_id_seq;
       public          postgres    false    277            �           0    0    rice_varieties_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.rice_varieties_id_seq OWNED BY public.rice_varieties.id;
          public          postgres    false    278                       1259    65735    rol    TABLE     w   CREATE TABLE public.rol (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion text
);
    DROP TABLE public.rol;
       public         heap    postgres    false                       1259    65740 
   rol_id_seq    SEQUENCE     �   CREATE SEQUENCE public.rol_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 !   DROP SEQUENCE public.rol_id_seq;
       public          postgres    false    279            �           0    0 
   rol_id_seq    SEQUENCE OWNED BY     9   ALTER SEQUENCE public.rol_id_seq OWNED BY public.rol.id;
          public          postgres    false    280                       1259    65741    rol_permiso    TABLE     b   CREATE TABLE public.rol_permiso (
    rol_id integer NOT NULL,
    permiso_id integer NOT NULL
);
    DROP TABLE public.rol_permiso;
       public         heap    postgres    false                       1259    65744    tarea_labor_cultural    TABLE     �  CREATE TABLE public.tarea_labor_cultural (
    id integer NOT NULL,
    fecha_estimada date NOT NULL,
    fecha_realizacion date,
    descripcion text,
    estado_id integer NOT NULL,
    es_mecanizable boolean NOT NULL,
    cultivo_id integer NOT NULL,
    labor_cultural_id integer NOT NULL,
    insumo_agricola_id integer,
    usuario_id integer NOT NULL,
    cantidad_insumo integer,
    maquinaria_agricola_id integer,
    precio_labor_cultural integer
);
 (   DROP TABLE public.tarea_labor_cultural;
       public         heap    postgres    false                       1259    65749    tarea_labor_cultural_id_seq    SEQUENCE     �   CREATE SEQUENCE public.tarea_labor_cultural_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 2   DROP SEQUENCE public.tarea_labor_cultural_id_seq;
       public          postgres    false    282            �           0    0    tarea_labor_cultural_id_seq    SEQUENCE OWNED BY     [   ALTER SEQUENCE public.tarea_labor_cultural_id_seq OWNED BY public.tarea_labor_cultural.id;
          public          postgres    false    283                       1259    65750    textura    TABLE     j   CREATE TABLE public.textura (
    id integer NOT NULL,
    descripcion character varying(255) NOT NULL
);
    DROP TABLE public.textura;
       public         heap    postgres    false                       1259    65753    textura_id_seq    SEQUENCE     �   CREATE SEQUENCE public.textura_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.textura_id_seq;
       public          postgres    false    284            �           0    0    textura_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.textura_id_seq OWNED BY public.textura.id;
          public          postgres    false    285                       1259    65754    tipo_insumo    TABLE     i   CREATE TABLE public.tipo_insumo (
    id integer NOT NULL,
    nombre character varying(255) NOT NULL
);
    DROP TABLE public.tipo_insumo;
       public         heap    postgres    false                       1259    65757    tipo_insumo_id_seq    SEQUENCE     �   CREATE SEQUENCE public.tipo_insumo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.tipo_insumo_id_seq;
       public          postgres    false    286            �           0    0    tipo_insumo_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.tipo_insumo_id_seq OWNED BY public.tipo_insumo.id;
          public          postgres    false    287                        1259    65758 
   tipo_suelo    TABLE     m   CREATE TABLE public.tipo_suelo (
    id integer NOT NULL,
    descripcion character varying(255) NOT NULL
);
    DROP TABLE public.tipo_suelo;
       public         heap    postgres    false            !           1259    65761    tipo_suelo_id_seq    SEQUENCE     �   CREATE SEQUENCE public.tipo_suelo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.tipo_suelo_id_seq;
       public          postgres    false    288            �           0    0    tipo_suelo_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.tipo_suelo_id_seq OWNED BY public.tipo_suelo.id;
          public          postgres    false    289            "           1259    65762    token    TABLE     �   CREATE TABLE public.token (
    user_id integer,
    access_toke character varying(450) NOT NULL,
    refresh_toke character varying(450) NOT NULL,
    status boolean,
    created_date timestamp without time zone
);
    DROP TABLE public.token;
       public         heap    postgres    false            #           1259    65767    unidad_area    TABLE     h   CREATE TABLE public.unidad_area (
    id integer NOT NULL,
    unidad character varying(50) NOT NULL
);
    DROP TABLE public.unidad_area;
       public         heap    postgres    false            $           1259    65770    unidad_area_id_seq    SEQUENCE     �   CREATE SEQUENCE public.unidad_area_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.unidad_area_id_seq;
       public          postgres    false    291            �           0    0    unidad_area_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.unidad_area_id_seq OWNED BY public.unidad_area.id;
          public          postgres    false    292            %           1259    65771    unidad_insumo    TABLE     j   CREATE TABLE public.unidad_insumo (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL
);
 !   DROP TABLE public.unidad_insumo;
       public         heap    postgres    false            &           1259    65774    unidad_insumo_id_seq    SEQUENCE     �   CREATE SEQUENCE public.unidad_insumo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.unidad_insumo_id_seq;
       public          postgres    false    293            �           0    0    unidad_insumo_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.unidad_insumo_id_seq OWNED BY public.unidad_insumo.id;
          public          postgres    false    294            '           1259    65775    unidad_peso    TABLE     o   CREATE TABLE public.unidad_peso (
    id integer NOT NULL,
    nombre_unidad character varying(20) NOT NULL
);
    DROP TABLE public.unidad_peso;
       public         heap    postgres    false            (           1259    65778    unidad_peso_id_seq    SEQUENCE     �   CREATE SEQUENCE public.unidad_peso_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.unidad_peso_id_seq;
       public          postgres    false    295            �           0    0    unidad_peso_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.unidad_peso_id_seq OWNED BY public.unidad_peso.id;
          public          postgres    false    296            )           1259    65779    usuario    TABLE       CREATE TABLE public.usuario (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    apellido character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    password character varying(255) NOT NULL,
    primer_login boolean DEFAULT true
);
    DROP TABLE public.usuario;
       public         heap    postgres    false            *           1259    65785    usuario_finca    TABLE     f   CREATE TABLE public.usuario_finca (
    usuario_id integer NOT NULL,
    finca_id integer NOT NULL
);
 !   DROP TABLE public.usuario_finca;
       public         heap    postgres    false            +           1259    65788    usuario_id_seq    SEQUENCE     �   CREATE SEQUENCE public.usuario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.usuario_id_seq;
       public          postgres    false    297            �           0    0    usuario_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.usuario_id_seq OWNED BY public.usuario.id;
          public          postgres    false    299            ,           1259    65789    usuario_rol    TABLE     i   CREATE TABLE public.usuario_rol (
    id integer NOT NULL,
    usuario_id integer,
    rol_id integer
);
    DROP TABLE public.usuario_rol;
       public         heap    postgres    false            -           1259    65792    usuario_rol_id_seq    SEQUENCE     �   CREATE SEQUENCE public.usuario_rol_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.usuario_rol_id_seq;
       public          postgres    false    300            �           0    0    usuario_rol_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.usuario_rol_id_seq OWNED BY public.usuario_rol.id;
          public          postgres    false    301            .           1259    65793    variedad_arroz    TABLE        CREATE TABLE public.variedad_arroz (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL,
    numero_registro_productor_ica character varying(50) NOT NULL,
    caracteristicas_variedad text,
    variedad_arroz_etapa_fenologica_id integer
);
 "   DROP TABLE public.variedad_arroz;
       public         heap    postgres    false            /           1259    65798    variedad_arroz_etapa_fenologica    TABLE     �   CREATE TABLE public.variedad_arroz_etapa_fenologica (
    variedad_arroz_id integer NOT NULL,
    etapa_fenologica_id integer,
    dias_duracion integer NOT NULL,
    id integer NOT NULL,
    nombre text
);
 3   DROP TABLE public.variedad_arroz_etapa_fenologica;
       public         heap    postgres    false            0           1259    65803 &   variedad_arroz_etapa_fenologica_id_seq    SEQUENCE     �   CREATE SEQUENCE public.variedad_arroz_etapa_fenologica_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 =   DROP SEQUENCE public.variedad_arroz_etapa_fenologica_id_seq;
       public          postgres    false    303            �           0    0 &   variedad_arroz_etapa_fenologica_id_seq    SEQUENCE OWNED BY     q   ALTER SEQUENCE public.variedad_arroz_etapa_fenologica_id_seq OWNED BY public.variedad_arroz_etapa_fenologica.id;
          public          postgres    false    304            1           1259    65804    variedad_arroz_id_seq    SEQUENCE     �   CREATE SEQUENCE public.variedad_arroz_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.variedad_arroz_id_seq;
       public          postgres    false    302            �           0    0    variedad_arroz_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.variedad_arroz_id_seq OWNED BY public.variedad_arroz.id;
          public          postgres    false    305                       2604    65805    agua id    DEFAULT     b   ALTER TABLE ONLY public.agua ALTER COLUMN id SET DEFAULT nextval('public.agua_id_seq'::regclass);
 6   ALTER TABLE public.agua ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    216    215            	           2604    65806    analisis_edafologico id    DEFAULT     �   ALTER TABLE ONLY public.analisis_edafologico ALTER COLUMN id SET DEFAULT nextval('public.analisis_edafologico_id_seq'::regclass);
 F   ALTER TABLE public.analisis_edafologico ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    218    217            ;           2604    66208    audit_logs id    DEFAULT     n   ALTER TABLE ONLY public.audit_logs ALTER COLUMN id SET DEFAULT nextval('public.audit_logs_id_seq'::regclass);
 <   ALTER TABLE public.audit_logs ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    306    307    307                       2604    65807    color id    DEFAULT     d   ALTER TABLE ONLY public.color ALTER COLUMN id SET DEFAULT nextval('public.color_id_seq'::regclass);
 7   ALTER TABLE public.color ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    220    219                       2604    65808 
   cosecha id    DEFAULT     h   ALTER TABLE ONLY public.cosecha ALTER COLUMN id SET DEFAULT nextval('public.cosecha_id_seq'::regclass);
 9   ALTER TABLE public.cosecha ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    222    221                       2604    65809    costos_adicionales id    DEFAULT     ~   ALTER TABLE ONLY public.costos_adicionales ALTER COLUMN id SET DEFAULT nextval('public.costos_adicionales_id_seq'::regclass);
 D   ALTER TABLE public.costos_adicionales ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    224    223                       2604    65810    costos_estimados id    DEFAULT     z   ALTER TABLE ONLY public.costos_estimados ALTER COLUMN id SET DEFAULT nextval('public.costos_estimados_id_seq'::regclass);
 B   ALTER TABLE public.costos_estimados ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    226    225                       2604    65811    costos_reales id    DEFAULT     t   ALTER TABLE ONLY public.costos_reales ALTER COLUMN id SET DEFAULT nextval('public.costos_reales_id_seq'::regclass);
 ?   ALTER TABLE public.costos_reales ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    228    227                       2604    65812 
   cultivo id    DEFAULT     h   ALTER TABLE ONLY public.cultivo ALTER COLUMN id SET DEFAULT nextval('public.cultivo_id_seq'::regclass);
 9   ALTER TABLE public.cultivo ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    230    229                       2604    65814    diagnostico_fitosanitario id    DEFAULT     �   ALTER TABLE ONLY public.diagnostico_fitosanitario ALTER COLUMN id SET DEFAULT nextval('public.diagnostico_fitosanitario_id_seq'::regclass);
 K   ALTER TABLE public.diagnostico_fitosanitario ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    232    231                       2604    65815 	   estado id    DEFAULT     f   ALTER TABLE ONLY public.estado ALTER COLUMN id SET DEFAULT nextval('public.estado_id_seq'::regclass);
 8   ALTER TABLE public.estado ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    234    233                       2604    65816    etapa_fenologica id    DEFAULT     z   ALTER TABLE ONLY public.etapa_fenologica ALTER COLUMN id SET DEFAULT nextval('public.etapa_fenologica_id_seq'::regclass);
 B   ALTER TABLE public.etapa_fenologica ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    236    235                       2604    65817    finca id    DEFAULT     d   ALTER TABLE ONLY public.finca ALTER COLUMN id SET DEFAULT nextval('public.finca_id_seq'::regclass);
 7   ALTER TABLE public.finca ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    238    237                       2604    65818 	   gastos id    DEFAULT     f   ALTER TABLE ONLY public.gastos ALTER COLUMN id SET DEFAULT nextval('public.gastos_id_seq'::regclass);
 8   ALTER TABLE public.gastos ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    242    239                       2604    65819 %   gastos_administrativos_financieros id    DEFAULT     �   ALTER TABLE ONLY public.gastos_administrativos_financieros ALTER COLUMN id SET DEFAULT nextval('public.gastos_administrativos_financieros_id_seq'::regclass);
 T   ALTER TABLE public.gastos_administrativos_financieros ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    241    240                       2604    65820    gastos_variables id    DEFAULT     z   ALTER TABLE ONLY public.gastos_variables ALTER COLUMN id SET DEFAULT nextval('public.gastos_variables_id_seq'::regclass);
 B   ALTER TABLE public.gastos_variables ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    244    243                       2604    65821    insumo_agricola id    DEFAULT     x   ALTER TABLE ONLY public.insumo_agricola ALTER COLUMN id SET DEFAULT nextval('public.insumo_agricola_id_seq'::regclass);
 A   ALTER TABLE public.insumo_agricola ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    246    245                       2604    65822    labor_cultural id    DEFAULT     v   ALTER TABLE ONLY public.labor_cultural ALTER COLUMN id SET DEFAULT nextval('public.labor_cultural_id_seq'::regclass);
 @   ALTER TABLE public.labor_cultural ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    248    247                       2604    65823    lote id    DEFAULT     b   ALTER TABLE ONLY public.lote ALTER COLUMN id SET DEFAULT nextval('public.lote_id_seq'::regclass);
 6   ALTER TABLE public.lote ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    250    249                       2604    65824    macronutriente id    DEFAULT     v   ALTER TABLE ONLY public.macronutriente ALTER COLUMN id SET DEFAULT nextval('public.macronutriente_id_seq'::regclass);
 @   ALTER TABLE public.macronutriente ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    252    251                        2604    65825    mano_obra id    DEFAULT     l   ALTER TABLE ONLY public.mano_obra ALTER COLUMN id SET DEFAULT nextval('public.mano_obra_id_seq'::regclass);
 ;   ALTER TABLE public.mano_obra ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    254    253            !           2604    65826    maquinaria_agricola id    DEFAULT     �   ALTER TABLE ONLY public.maquinaria_agricola ALTER COLUMN id SET DEFAULT nextval('public.maquinaria_agricola_id_seq'::regclass);
 E   ALTER TABLE public.maquinaria_agricola ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    256    255            "           2604    65827    micronutriente id    DEFAULT     v   ALTER TABLE ONLY public.micronutriente ALTER COLUMN id SET DEFAULT nextval('public.micronutriente_id_seq'::regclass);
 @   ALTER TABLE public.micronutriente ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    258    257            #           2604    65828    monitoreos id    DEFAULT     n   ALTER TABLE ONLY public.monitoreos ALTER COLUMN id SET DEFAULT nextval('public.monitoreos_id_seq'::regclass);
 <   ALTER TABLE public.monitoreos ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    260    259            $           2604    65829    operacion_mecanizacion id    DEFAULT     �   ALTER TABLE ONLY public.operacion_mecanizacion ALTER COLUMN id SET DEFAULT nextval('public.operacion_mecanizacion_id_seq'::regclass);
 H   ALTER TABLE public.operacion_mecanizacion ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    262    261            %           2604    65830    parametro_biologico id    DEFAULT     �   ALTER TABLE ONLY public.parametro_biologico ALTER COLUMN id SET DEFAULT nextval('public.parametro_biologico_id_seq'::regclass);
 E   ALTER TABLE public.parametro_biologico ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    264    263            &           2604    65831    parametro_fisico id    DEFAULT     z   ALTER TABLE ONLY public.parametro_fisico ALTER COLUMN id SET DEFAULT nextval('public.parametro_fisico_id_seq'::regclass);
 B   ALTER TABLE public.parametro_fisico ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    266    265            '           2604    65832    parametro_quimico id    DEFAULT     |   ALTER TABLE ONLY public.parametro_quimico ALTER COLUMN id SET DEFAULT nextval('public.parametro_quimico_id_seq'::regclass);
 C   ALTER TABLE public.parametro_quimico ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    268    267            (           2604    65833    password_resets id    DEFAULT     x   ALTER TABLE ONLY public.password_resets ALTER COLUMN id SET DEFAULT nextval('public.password_resets_id_seq'::regclass);
 A   ALTER TABLE public.password_resets ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    270    269            )           2604    65834 
   permiso id    DEFAULT     h   ALTER TABLE ONLY public.permiso ALTER COLUMN id SET DEFAULT nextval('public.permiso_id_seq'::regclass);
 9   ALTER TABLE public.permiso ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    272    271            *           2604    65835    phenological_stages id    DEFAULT     �   ALTER TABLE ONLY public.phenological_stages ALTER COLUMN id SET DEFAULT nextval('public.phenological_stages_id_seq'::regclass);
 E   ALTER TABLE public.phenological_stages ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    274    273            +           2604    65836    registro_meteorologico id    DEFAULT     �   ALTER TABLE ONLY public.registro_meteorologico ALTER COLUMN id SET DEFAULT nextval('public.registro_meteorologico_id_seq'::regclass);
 H   ALTER TABLE public.registro_meteorologico ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    276    275            -           2604    65837    rice_varieties id    DEFAULT     v   ALTER TABLE ONLY public.rice_varieties ALTER COLUMN id SET DEFAULT nextval('public.rice_varieties_id_seq'::regclass);
 @   ALTER TABLE public.rice_varieties ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    278    277            .           2604    65838    rol id    DEFAULT     `   ALTER TABLE ONLY public.rol ALTER COLUMN id SET DEFAULT nextval('public.rol_id_seq'::regclass);
 5   ALTER TABLE public.rol ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    280    279            /           2604    65839    tarea_labor_cultural id    DEFAULT     �   ALTER TABLE ONLY public.tarea_labor_cultural ALTER COLUMN id SET DEFAULT nextval('public.tarea_labor_cultural_id_seq'::regclass);
 F   ALTER TABLE public.tarea_labor_cultural ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    283    282            0           2604    65840 
   textura id    DEFAULT     h   ALTER TABLE ONLY public.textura ALTER COLUMN id SET DEFAULT nextval('public.textura_id_seq'::regclass);
 9   ALTER TABLE public.textura ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    285    284            1           2604    65841    tipo_insumo id    DEFAULT     p   ALTER TABLE ONLY public.tipo_insumo ALTER COLUMN id SET DEFAULT nextval('public.tipo_insumo_id_seq'::regclass);
 =   ALTER TABLE public.tipo_insumo ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    287    286            2           2604    65842    tipo_suelo id    DEFAULT     n   ALTER TABLE ONLY public.tipo_suelo ALTER COLUMN id SET DEFAULT nextval('public.tipo_suelo_id_seq'::regclass);
 <   ALTER TABLE public.tipo_suelo ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    289    288            3           2604    65843    unidad_area id    DEFAULT     p   ALTER TABLE ONLY public.unidad_area ALTER COLUMN id SET DEFAULT nextval('public.unidad_area_id_seq'::regclass);
 =   ALTER TABLE public.unidad_area ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    292    291            4           2604    65844    unidad_insumo id    DEFAULT     t   ALTER TABLE ONLY public.unidad_insumo ALTER COLUMN id SET DEFAULT nextval('public.unidad_insumo_id_seq'::regclass);
 ?   ALTER TABLE public.unidad_insumo ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    294    293            5           2604    65845    unidad_peso id    DEFAULT     p   ALTER TABLE ONLY public.unidad_peso ALTER COLUMN id SET DEFAULT nextval('public.unidad_peso_id_seq'::regclass);
 =   ALTER TABLE public.unidad_peso ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    296    295            6           2604    65846 
   usuario id    DEFAULT     h   ALTER TABLE ONLY public.usuario ALTER COLUMN id SET DEFAULT nextval('public.usuario_id_seq'::regclass);
 9   ALTER TABLE public.usuario ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    299    297            8           2604    65847    usuario_rol id    DEFAULT     p   ALTER TABLE ONLY public.usuario_rol ALTER COLUMN id SET DEFAULT nextval('public.usuario_rol_id_seq'::regclass);
 =   ALTER TABLE public.usuario_rol ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    301    300            9           2604    65848    variedad_arroz id    DEFAULT     v   ALTER TABLE ONLY public.variedad_arroz ALTER COLUMN id SET DEFAULT nextval('public.variedad_arroz_id_seq'::regclass);
 @   ALTER TABLE public.variedad_arroz ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    305    302            :           2604    65849 "   variedad_arroz_etapa_fenologica id    DEFAULT     �   ALTER TABLE ONLY public.variedad_arroz_etapa_fenologica ALTER COLUMN id SET DEFAULT nextval('public.variedad_arroz_etapa_fenologica_id_seq'::regclass);
 Q   ALTER TABLE public.variedad_arroz_etapa_fenologica ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    304    303            n          0    65567    agua 
   TABLE DATA           �   COPY public.agua (id, costo_instalacion_agua_real, costo_instalacion_agua_estimado, costo_consumo_agua_real, costo_consumo_agua_estimado, consumo_energia_real, consumo_energia_estimada) FROM stdin;
    public          postgres    false    215   m�      p          0    65571    analisis_edafologico 
   TABLE DATA           �   COPY public.analisis_edafologico (id, lote_id, fecha_analisis, tipo_suelo_id, archivo_reporte, creado_en, actualizado_en) FROM stdin;
    public          postgres    false    217   ��      �          0    66205 
   audit_logs 
   TABLE DATA           r   COPY public.audit_logs (id, table_name, operation_type, record_id, changed_data, operation_timestamp) FROM stdin;
    public          postgres    false    307   �      r          0    65579    color 
   TABLE DATA           0   COPY public.color (id, descripcion) FROM stdin;
    public          postgres    false    219    �      t          0    65583    cosecha 
   TABLE DATA           �   COPY public.cosecha (id, cultivo_id, fecha_estimada_cosecha, fecha_cosecha, precio_carga_mercado, gasto_transporte_cosecha, gasto_recoleccion, cantidad_producida_cosecha, venta_cosecha) FROM stdin;
    public          postgres    false    221   D�      v          0    65587    costos_adicionales 
   TABLE DATA           �   COPY public.costos_adicionales (id, costo_capacitacion_real, costo_capacitacion_estimado, costo_control_roedores_real, costo_control_roedores_estimado) FROM stdin;
    public          postgres    false    223   ��      x          0    65591    costos_estimados 
   TABLE DATA           �   COPY public.costos_estimados (id, cantidad_insumo, costo_insumo, horas_de_uso_de_maquinaria, costo_maquinaria, numero_trabajadores_por_dia, numero_dias_trabajados, costo_mano_obra, tarea_labor_id) FROM stdin;
    public          postgres    false    225   ��      z          0    65595    costos_reales 
   TABLE DATA           �   COPY public.costos_reales (id, cantidad_insumo, costo_insumo, horas_de_uso_de_maquinaria, costo_maquinaria, numero_trabajadores_por_dia, numero_dias_trabajados, costo_mano_obra, tarea_labor_id) FROM stdin;
    public          postgres    false    227   ��      |          0    65599    cultivo 
   TABLE DATA           x   COPY public.cultivo (id, nombre_cultivo, variedad_id, lote_id, fecha_siembra, fecha_estimada_cosecha, slug) FROM stdin;
    public          postgres    false    229   ��      ~          0    65609    diagnostico_fitosanitario 
   TABLE DATA           �   COPY public.diagnostico_fitosanitario (id, resultado_ia, ruta, cultivo_id, fecha_diagnostico, confianza_promedio, tipo_problema, imagenes_analizadas, exportado, comparacion_diagnostico) FROM stdin;
    public          postgres    false    231   I�      �          0    65617    estado 
   TABLE DATA           9   COPY public.estado (id, nombre, descripcion) FROM stdin;
    public          postgres    false    233   ��      �          0    65623    etapa_fenologica 
   TABLE DATA           <   COPY public.etapa_fenologica (id, nombre, fase) FROM stdin;
    public          postgres    false    235   *�      �          0    65627    finca 
   TABLE DATA           w   COPY public.finca (id, nombre, ubicacion, area_total, latitud, longitud, slug, ciudad, departamento, pais) FROM stdin;
    public          postgres    false    237   ~�      �          0    65633    gastos 
   TABLE DATA           O   COPY public.gastos (id, cultivo_id, concepto, descripcion, precio) FROM stdin;
    public          postgres    false    239   �      �          0    65638 "   gastos_administrativos_financieros 
   TABLE DATA           �   COPY public.gastos_administrativos_financieros (id, costo_impuestos_real, costo_impuestos_estimado, costo_seguros_real, costo_seguros_estimado) FROM stdin;
    public          postgres    false    240   ��      �          0    65643    gastos_variables 
   TABLE DATA           �   COPY public.gastos_variables (id, id_costos_adicionales, id_agua, id_gastos_administrativos_financieros, descripcion) FROM stdin;
    public          postgres    false    243   ��      �          0    65649    insumo_agricola 
   TABLE DATA           �   COPY public.insumo_agricola (id, nombre, descripcion, costo_unitario, cantidad, unidad_id, precio_unitario_estimado, cultivo_id, cantidad_estimada, tipo_insumo_id) FROM stdin;
    public          postgres    false    245   ��      �          0    65656    labor_cultural 
   TABLE DATA           �   COPY public.labor_cultural (id, nombre, descripcion, precio_hectaria, precio_hectaria_estimada, id_etapa_fenologica) FROM stdin;
    public          postgres    false    247   ��      �          0    65662    lote 
   TABLE DATA           �   COPY public.lote (id, nombre, finca_id, area, latitud, longitud, slug, costo_arriendo_real, costo_arriendo_estimado, arriendo_real) FROM stdin;
    public          postgres    false    249   S�      �          0    65666    macronutriente 
   TABLE DATA           V   COPY public.macronutriente (id, parametro_quimico_id, n, p, k, ca, mg, s) FROM stdin;
    public          postgres    false    251   ��      �          0    65670 	   mano_obra 
   TABLE DATA           G   COPY public.mano_obra (id, nombre, descripcion, costo_dia) FROM stdin;
    public          postgres    false    253   ��      �          0    65676    maquinaria_agricola 
   TABLE DATA           g   COPY public.maquinaria_agricola (id, nombre, descripcion, costo_hora, costo_hora_estimado) FROM stdin;
    public          postgres    false    255   ��      �          0    65682    micronutriente 
   TABLE DATA           U   COPY public.micronutriente (id, parametro_quimico_id, fe, cu, mn, zn, b) FROM stdin;
    public          postgres    false    257   -�      �          0    65686 
   monitoreos 
   TABLE DATA           �   COPY public.monitoreos (id, tipo, variedad_arroz_etapa_fenologica_id, recomendacion, crop_id, fecha_programada, fecha_finalizacion, estado) FROM stdin;
    public          postgres    false    259   J�      �          0    65692    operacion_mecanizacion 
   TABLE DATA           s   COPY public.operacion_mecanizacion (id, tarea_labor_id, nombre_mecanizacion, maquinaria_id, horas_uso) FROM stdin;
    public          postgres    false    261   ��      �          0    65696    parametro_biologico 
   TABLE DATA           t   COPY public.parametro_biologico (id, analisis_edafologico_id, biomasa_microbiana, actividad_enzimatica) FROM stdin;
    public          postgres    false    263   ��      �          0    65700    parametro_fisico 
   TABLE DATA           �   COPY public.parametro_fisico (id, analisis_edafologico_id, textura_id, densidad_aparente, profundidad_efectiva, color_id) FROM stdin;
    public          postgres    false    265   �      �          0    65704    parametro_quimico 
   TABLE DATA           �   COPY public.parametro_quimico (id, analisis_edafologico_id, ph, conductividad_electrica, materia_organica, capacidad_intercambio_cationico) FROM stdin;
    public          postgres    false    267   "�      �          0    65708    password_resets 
   TABLE DATA           G   COPY public.password_resets (id, email, token, created_at) FROM stdin;
    public          postgres    false    269   ?�      �          0    65714    permiso 
   TABLE DATA           :   COPY public.permiso (id, nombre, descripcion) FROM stdin;
    public          postgres    false    271   ��      �          0    65720    phenological_stages 
   TABLE DATA           ]   COPY public.phenological_stages (id, rice_variety_id, stage_name, duration_days) FROM stdin;
    public          postgres    false    273   ��      �          0    65724    registro_meteorologico 
   TABLE DATA           �   COPY public.registro_meteorologico (id, lote_id, fecha, temperatura, presion_atmosferica, humedad, precipitacion, indice_ultravioleta, horas_sol, fuente_datos, hora, api_respuesta, creado_en) FROM stdin;
    public          postgres    false    275          �          0    65731    rice_varieties 
   TABLE DATA           2   COPY public.rice_varieties (id, name) FROM stdin;
    public          postgres    false    277   �      �          0    65735    rol 
   TABLE DATA           6   COPY public.rol (id, nombre, descripcion) FROM stdin;
    public          postgres    false    279   �      �          0    65741    rol_permiso 
   TABLE DATA           9   COPY public.rol_permiso (rol_id, permiso_id) FROM stdin;
    public          postgres    false    281   +      �          0    65744    tarea_labor_cultural 
   TABLE DATA           �   COPY public.tarea_labor_cultural (id, fecha_estimada, fecha_realizacion, descripcion, estado_id, es_mecanizable, cultivo_id, labor_cultural_id, insumo_agricola_id, usuario_id, cantidad_insumo, maquinaria_agricola_id, precio_labor_cultural) FROM stdin;
    public          postgres    false    282         �          0    65750    textura 
   TABLE DATA           2   COPY public.textura (id, descripcion) FROM stdin;
    public          postgres    false    284   �      �          0    65754    tipo_insumo 
   TABLE DATA           1   COPY public.tipo_insumo (id, nombre) FROM stdin;
    public          postgres    false    286   �      �          0    65758 
   tipo_suelo 
   TABLE DATA           5   COPY public.tipo_suelo (id, descripcion) FROM stdin;
    public          postgres    false    288   *      �          0    65762    token 
   TABLE DATA           Y   COPY public.token (user_id, access_toke, refresh_toke, status, created_date) FROM stdin;
    public          postgres    false    290   a      �          0    65767    unidad_area 
   TABLE DATA           1   COPY public.unidad_area (id, unidad) FROM stdin;
    public          postgres    false    291   q      �          0    65771    unidad_insumo 
   TABLE DATA           3   COPY public.unidad_insumo (id, nombre) FROM stdin;
    public          postgres    false    293   �      �          0    65775    unidad_peso 
   TABLE DATA           8   COPY public.unidad_peso (id, nombre_unidad) FROM stdin;
    public          postgres    false    295   �      �          0    65779    usuario 
   TABLE DATA           V   COPY public.usuario (id, nombre, apellido, email, password, primer_login) FROM stdin;
    public          postgres    false    297   �      �          0    65785    usuario_finca 
   TABLE DATA           =   COPY public.usuario_finca (usuario_id, finca_id) FROM stdin;
    public          postgres    false    298   �      �          0    65789    usuario_rol 
   TABLE DATA           =   COPY public.usuario_rol (id, usuario_id, rol_id) FROM stdin;
    public          postgres    false    300   �      �          0    65793    variedad_arroz 
   TABLE DATA           �   COPY public.variedad_arroz (id, nombre, numero_registro_productor_ica, caracteristicas_variedad, variedad_arroz_etapa_fenologica_id) FROM stdin;
    public          postgres    false    302         �          0    65798    variedad_arroz_etapa_fenologica 
   TABLE DATA           |   COPY public.variedad_arroz_etapa_fenologica (variedad_arroz_id, etapa_fenologica_id, dias_duracion, id, nombre) FROM stdin;
    public          postgres    false    303   b      �           0    0    agua_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.agua_id_seq', 1, false);
          public          postgres    false    216            �           0    0    analisis_edafologico_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.analisis_edafologico_id_seq', 1, true);
          public          postgres    false    218                        0    0    audit_logs_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.audit_logs_id_seq', 1, false);
          public          postgres    false    306                       0    0    color_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.color_id_seq', 1, true);
          public          postgres    false    220                       0    0    cosecha_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.cosecha_id_seq', 3, true);
          public          postgres    false    222                       0    0    costos_adicionales_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.costos_adicionales_id_seq', 1, false);
          public          postgres    false    224                       0    0    costos_estimados_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.costos_estimados_id_seq', 1, false);
          public          postgres    false    226                       0    0    costos_reales_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.costos_reales_id_seq', 1, false);
          public          postgres    false    228                       0    0    cultivo_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.cultivo_id_seq', 4, true);
          public          postgres    false    230                       0    0     diagnostico_fitosanitario_id_seq    SEQUENCE SET     N   SELECT pg_catalog.setval('public.diagnostico_fitosanitario_id_seq', 2, true);
          public          postgres    false    232                       0    0    estado_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.estado_id_seq', 2, true);
          public          postgres    false    234            	           0    0    etapa_fenologica_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.etapa_fenologica_id_seq', 4, true);
          public          postgres    false    236            
           0    0    finca_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.finca_id_seq', 4, true);
          public          postgres    false    238                       0    0 )   gastos_administrativos_financieros_id_seq    SEQUENCE SET     X   SELECT pg_catalog.setval('public.gastos_administrativos_financieros_id_seq', 1, false);
          public          postgres    false    241                       0    0    gastos_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.gastos_id_seq', 10, true);
          public          postgres    false    242                       0    0    gastos_variables_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.gastos_variables_id_seq', 1, false);
          public          postgres    false    244                       0    0    insumo_agricola_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.insumo_agricola_id_seq', 12, true);
          public          postgres    false    246                       0    0    labor_cultural_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.labor_cultural_id_seq', 10, true);
          public          postgres    false    248                       0    0    lote_id_seq    SEQUENCE SET     9   SELECT pg_catalog.setval('public.lote_id_seq', 4, true);
          public          postgres    false    250                       0    0    macronutriente_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.macronutriente_id_seq', 1, true);
          public          postgres    false    252                       0    0    mano_obra_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.mano_obra_id_seq', 1, false);
          public          postgres    false    254                       0    0    maquinaria_agricola_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.maquinaria_agricola_id_seq', 1, true);
          public          postgres    false    256                       0    0    micronutriente_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.micronutriente_id_seq', 1, true);
          public          postgres    false    258                       0    0    monitoreos_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.monitoreos_id_seq', 6, true);
          public          postgres    false    260                       0    0    operacion_mecanizacion_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.operacion_mecanizacion_id_seq', 1, false);
          public          postgres    false    262                       0    0    parametro_biologico_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.parametro_biologico_id_seq', 1, true);
          public          postgres    false    264                       0    0    parametro_fisico_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.parametro_fisico_id_seq', 1, true);
          public          postgres    false    266                       0    0    parametro_quimico_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.parametro_quimico_id_seq', 1, true);
          public          postgres    false    268                       0    0    password_resets_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.password_resets_id_seq', 8, true);
          public          postgres    false    270                       0    0    permiso_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.permiso_id_seq', 3, true);
          public          postgres    false    272                       0    0    phenological_stages_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.phenological_stages_id_seq', 1, false);
          public          postgres    false    274                       0    0    registro_meteorologico_id_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public.registro_meteorologico_id_seq', 9, true);
          public          postgres    false    276                       0    0    rice_varieties_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.rice_varieties_id_seq', 1, false);
          public          postgres    false    278                       0    0 
   rol_id_seq    SEQUENCE SET     9   SELECT pg_catalog.setval('public.rol_id_seq', 73, true);
          public          postgres    false    280                        0    0    tarea_labor_cultural_id_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public.tarea_labor_cultural_id_seq', 30, true);
          public          postgres    false    283            !           0    0    textura_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.textura_id_seq', 1, true);
          public          postgres    false    285            "           0    0    tipo_insumo_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.tipo_insumo_id_seq', 4, true);
          public          postgres    false    287            #           0    0    tipo_suelo_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.tipo_suelo_id_seq', 2, true);
          public          postgres    false    289            $           0    0    unidad_area_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.unidad_area_id_seq', 1, false);
          public          postgres    false    292            %           0    0    unidad_insumo_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.unidad_insumo_id_seq', 1, false);
          public          postgres    false    294            &           0    0    unidad_peso_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.unidad_peso_id_seq', 1, false);
          public          postgres    false    296            '           0    0    usuario_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.usuario_id_seq', 152, true);
          public          postgres    false    299            (           0    0    usuario_rol_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.usuario_rol_id_seq', 44, true);
          public          postgres    false    301            )           0    0 &   variedad_arroz_etapa_fenologica_id_seq    SEQUENCE SET     T   SELECT pg_catalog.setval('public.variedad_arroz_etapa_fenologica_id_seq', 6, true);
          public          postgres    false    304            *           0    0    variedad_arroz_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.variedad_arroz_id_seq', 2, true);
          public          postgres    false    305            =           2606    65851    agua agua_pkey 
   CONSTRAINT     L   ALTER TABLE ONLY public.agua
    ADD CONSTRAINT agua_pkey PRIMARY KEY (id);
 8   ALTER TABLE ONLY public.agua DROP CONSTRAINT agua_pkey;
       public            postgres    false    215            ?           2606    65853 .   analisis_edafologico analisis_edafologico_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY public.analisis_edafologico
    ADD CONSTRAINT analisis_edafologico_pkey PRIMARY KEY (id);
 X   ALTER TABLE ONLY public.analisis_edafologico DROP CONSTRAINT analisis_edafologico_pkey;
       public            postgres    false    217            �           2606    66212    audit_logs audit_logs_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.audit_logs DROP CONSTRAINT audit_logs_pkey;
       public            postgres    false    307            A           2606    65855    color color_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.color
    ADD CONSTRAINT color_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.color DROP CONSTRAINT color_pkey;
       public            postgres    false    219            C           2606    65857    cosecha cosecha_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.cosecha
    ADD CONSTRAINT cosecha_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.cosecha DROP CONSTRAINT cosecha_pkey;
       public            postgres    false    221            E           2606    65859 *   costos_adicionales costos_adicionales_pkey 
   CONSTRAINT     h   ALTER TABLE ONLY public.costos_adicionales
    ADD CONSTRAINT costos_adicionales_pkey PRIMARY KEY (id);
 T   ALTER TABLE ONLY public.costos_adicionales DROP CONSTRAINT costos_adicionales_pkey;
       public            postgres    false    223            G           2606    65861 &   costos_estimados costos_estimados_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.costos_estimados
    ADD CONSTRAINT costos_estimados_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.costos_estimados DROP CONSTRAINT costos_estimados_pkey;
       public            postgres    false    225            I           2606    65863 4   costos_estimados costos_estimados_tarea_labor_id_key 
   CONSTRAINT     y   ALTER TABLE ONLY public.costos_estimados
    ADD CONSTRAINT costos_estimados_tarea_labor_id_key UNIQUE (tarea_labor_id);
 ^   ALTER TABLE ONLY public.costos_estimados DROP CONSTRAINT costos_estimados_tarea_labor_id_key;
       public            postgres    false    225            K           2606    65865     costos_reales costos_reales_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.costos_reales
    ADD CONSTRAINT costos_reales_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.costos_reales DROP CONSTRAINT costos_reales_pkey;
       public            postgres    false    227            M           2606    65867 .   costos_reales costos_reales_tarea_labor_id_key 
   CONSTRAINT     s   ALTER TABLE ONLY public.costos_reales
    ADD CONSTRAINT costos_reales_tarea_labor_id_key UNIQUE (tarea_labor_id);
 X   ALTER TABLE ONLY public.costos_reales DROP CONSTRAINT costos_reales_tarea_labor_id_key;
       public            postgres    false    227            O           2606    65869    cultivo cultivo_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.cultivo
    ADD CONSTRAINT cultivo_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.cultivo DROP CONSTRAINT cultivo_pkey;
       public            postgres    false    229            Q           2606    65873 8   diagnostico_fitosanitario diagnostico_fitosanitario_pkey 
   CONSTRAINT     v   ALTER TABLE ONLY public.diagnostico_fitosanitario
    ADD CONSTRAINT diagnostico_fitosanitario_pkey PRIMARY KEY (id);
 b   ALTER TABLE ONLY public.diagnostico_fitosanitario DROP CONSTRAINT diagnostico_fitosanitario_pkey;
       public            postgres    false    231            S           2606    65875    estado estado_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.estado
    ADD CONSTRAINT estado_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.estado DROP CONSTRAINT estado_pkey;
       public            postgres    false    233            U           2606    65877 &   etapa_fenologica etapa_fenologica_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.etapa_fenologica
    ADD CONSTRAINT etapa_fenologica_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.etapa_fenologica DROP CONSTRAINT etapa_fenologica_pkey;
       public            postgres    false    235            W           2606    65879    finca finca_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.finca
    ADD CONSTRAINT finca_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.finca DROP CONSTRAINT finca_pkey;
       public            postgres    false    237            [           2606    65881 J   gastos_administrativos_financieros gastos_administrativos_financieros_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.gastos_administrativos_financieros
    ADD CONSTRAINT gastos_administrativos_financieros_pkey PRIMARY KEY (id);
 t   ALTER TABLE ONLY public.gastos_administrativos_financieros DROP CONSTRAINT gastos_administrativos_financieros_pkey;
       public            postgres    false    240            Y           2606    65883    gastos gastos_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.gastos
    ADD CONSTRAINT gastos_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.gastos DROP CONSTRAINT gastos_pkey;
       public            postgres    false    239            ]           2606    65885 &   gastos_variables gastos_variables_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.gastos_variables
    ADD CONSTRAINT gastos_variables_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.gastos_variables DROP CONSTRAINT gastos_variables_pkey;
       public            postgres    false    243            _           2606    65887 $   insumo_agricola insumo_agricola_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.insumo_agricola
    ADD CONSTRAINT insumo_agricola_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.insumo_agricola DROP CONSTRAINT insumo_agricola_pkey;
       public            postgres    false    245            a           2606    65889 "   labor_cultural labor_cultural_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.labor_cultural
    ADD CONSTRAINT labor_cultural_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.labor_cultural DROP CONSTRAINT labor_cultural_pkey;
       public            postgres    false    247            c           2606    65891    lote lote_pkey 
   CONSTRAINT     L   ALTER TABLE ONLY public.lote
    ADD CONSTRAINT lote_pkey PRIMARY KEY (id);
 8   ALTER TABLE ONLY public.lote DROP CONSTRAINT lote_pkey;
       public            postgres    false    249            e           2606    65893 "   macronutriente macronutriente_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.macronutriente
    ADD CONSTRAINT macronutriente_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.macronutriente DROP CONSTRAINT macronutriente_pkey;
       public            postgres    false    251            g           2606    65895    mano_obra mano_obra_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.mano_obra
    ADD CONSTRAINT mano_obra_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.mano_obra DROP CONSTRAINT mano_obra_pkey;
       public            postgres    false    253            i           2606    65897 ,   maquinaria_agricola maquinaria_agricola_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.maquinaria_agricola
    ADD CONSTRAINT maquinaria_agricola_pkey PRIMARY KEY (id);
 V   ALTER TABLE ONLY public.maquinaria_agricola DROP CONSTRAINT maquinaria_agricola_pkey;
       public            postgres    false    255            k           2606    65899 "   micronutriente micronutriente_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.micronutriente
    ADD CONSTRAINT micronutriente_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.micronutriente DROP CONSTRAINT micronutriente_pkey;
       public            postgres    false    257            m           2606    65901    monitoreos monitoreos_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.monitoreos
    ADD CONSTRAINT monitoreos_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.monitoreos DROP CONSTRAINT monitoreos_pkey;
       public            postgres    false    259            o           2606    65903 2   operacion_mecanizacion operacion_mecanizacion_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY public.operacion_mecanizacion
    ADD CONSTRAINT operacion_mecanizacion_pkey PRIMARY KEY (id);
 \   ALTER TABLE ONLY public.operacion_mecanizacion DROP CONSTRAINT operacion_mecanizacion_pkey;
       public            postgres    false    261            q           2606    65905 @   operacion_mecanizacion operacion_mecanizacion_tarea_labor_id_key 
   CONSTRAINT     �   ALTER TABLE ONLY public.operacion_mecanizacion
    ADD CONSTRAINT operacion_mecanizacion_tarea_labor_id_key UNIQUE (tarea_labor_id);
 j   ALTER TABLE ONLY public.operacion_mecanizacion DROP CONSTRAINT operacion_mecanizacion_tarea_labor_id_key;
       public            postgres    false    261            s           2606    65907 ,   parametro_biologico parametro_biologico_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.parametro_biologico
    ADD CONSTRAINT parametro_biologico_pkey PRIMARY KEY (id);
 V   ALTER TABLE ONLY public.parametro_biologico DROP CONSTRAINT parametro_biologico_pkey;
       public            postgres    false    263            u           2606    65909 &   parametro_fisico parametro_fisico_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.parametro_fisico
    ADD CONSTRAINT parametro_fisico_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.parametro_fisico DROP CONSTRAINT parametro_fisico_pkey;
       public            postgres    false    265            w           2606    65911 (   parametro_quimico parametro_quimico_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.parametro_quimico
    ADD CONSTRAINT parametro_quimico_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.parametro_quimico DROP CONSTRAINT parametro_quimico_pkey;
       public            postgres    false    267            |           2606    65913 $   password_resets password_resets_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.password_resets
    ADD CONSTRAINT password_resets_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.password_resets DROP CONSTRAINT password_resets_pkey;
       public            postgres    false    269            ~           2606    65915    permiso permiso_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.permiso
    ADD CONSTRAINT permiso_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.permiso DROP CONSTRAINT permiso_pkey;
       public            postgres    false    271            �           2606    65917 ,   phenological_stages phenological_stages_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.phenological_stages
    ADD CONSTRAINT phenological_stages_pkey PRIMARY KEY (id);
 V   ALTER TABLE ONLY public.phenological_stages DROP CONSTRAINT phenological_stages_pkey;
       public            postgres    false    273            �           2606    65919 2   registro_meteorologico registro_meteorologico_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY public.registro_meteorologico
    ADD CONSTRAINT registro_meteorologico_pkey PRIMARY KEY (id);
 \   ALTER TABLE ONLY public.registro_meteorologico DROP CONSTRAINT registro_meteorologico_pkey;
       public            postgres    false    275            �           2606    65921 "   rice_varieties rice_varieties_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.rice_varieties
    ADD CONSTRAINT rice_varieties_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.rice_varieties DROP CONSTRAINT rice_varieties_pkey;
       public            postgres    false    277            �           2606    65923    rol_permiso rol_permiso_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.rol_permiso
    ADD CONSTRAINT rol_permiso_pkey PRIMARY KEY (rol_id, permiso_id);
 F   ALTER TABLE ONLY public.rol_permiso DROP CONSTRAINT rol_permiso_pkey;
       public            postgres    false    281    281            �           2606    65925    rol rol_pkey 
   CONSTRAINT     J   ALTER TABLE ONLY public.rol
    ADD CONSTRAINT rol_pkey PRIMARY KEY (id);
 6   ALTER TABLE ONLY public.rol DROP CONSTRAINT rol_pkey;
       public            postgres    false    279            �           2606    65927 .   tarea_labor_cultural tarea_labor_cultural_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY public.tarea_labor_cultural
    ADD CONSTRAINT tarea_labor_cultural_pkey PRIMARY KEY (id);
 X   ALTER TABLE ONLY public.tarea_labor_cultural DROP CONSTRAINT tarea_labor_cultural_pkey;
       public            postgres    false    282            �           2606    65929    textura textura_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.textura
    ADD CONSTRAINT textura_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.textura DROP CONSTRAINT textura_pkey;
       public            postgres    false    284            �           2606    65931 "   tipo_insumo tipo_insumo_nombre_key 
   CONSTRAINT     _   ALTER TABLE ONLY public.tipo_insumo
    ADD CONSTRAINT tipo_insumo_nombre_key UNIQUE (nombre);
 L   ALTER TABLE ONLY public.tipo_insumo DROP CONSTRAINT tipo_insumo_nombre_key;
       public            postgres    false    286            �           2606    65933    tipo_insumo tipo_insumo_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.tipo_insumo
    ADD CONSTRAINT tipo_insumo_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.tipo_insumo DROP CONSTRAINT tipo_insumo_pkey;
       public            postgres    false    286            �           2606    65935    tipo_suelo tipo_suelo_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.tipo_suelo
    ADD CONSTRAINT tipo_suelo_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.tipo_suelo DROP CONSTRAINT tipo_suelo_pkey;
       public            postgres    false    288            �           2606    65937    token token_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.token
    ADD CONSTRAINT token_pkey PRIMARY KEY (access_toke);
 :   ALTER TABLE ONLY public.token DROP CONSTRAINT token_pkey;
       public            postgres    false    290            �           2606    65939    unidad_area unidad_area_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.unidad_area
    ADD CONSTRAINT unidad_area_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.unidad_area DROP CONSTRAINT unidad_area_pkey;
       public            postgres    false    291            �           2606    65941     unidad_insumo unidad_insumo_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.unidad_insumo
    ADD CONSTRAINT unidad_insumo_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.unidad_insumo DROP CONSTRAINT unidad_insumo_pkey;
       public            postgres    false    293            �           2606    65943 )   unidad_peso unidad_peso_nombre_unidad_key 
   CONSTRAINT     m   ALTER TABLE ONLY public.unidad_peso
    ADD CONSTRAINT unidad_peso_nombre_unidad_key UNIQUE (nombre_unidad);
 S   ALTER TABLE ONLY public.unidad_peso DROP CONSTRAINT unidad_peso_nombre_unidad_key;
       public            postgres    false    295            �           2606    65945    unidad_peso unidad_peso_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.unidad_peso
    ADD CONSTRAINT unidad_peso_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.unidad_peso DROP CONSTRAINT unidad_peso_pkey;
       public            postgres    false    295            �           2606    65947    usuario usuario_email_key 
   CONSTRAINT     U   ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_email_key UNIQUE (email);
 C   ALTER TABLE ONLY public.usuario DROP CONSTRAINT usuario_email_key;
       public            postgres    false    297            �           2606    65949     usuario_finca usuario_finca_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY public.usuario_finca
    ADD CONSTRAINT usuario_finca_pkey PRIMARY KEY (usuario_id, finca_id);
 J   ALTER TABLE ONLY public.usuario_finca DROP CONSTRAINT usuario_finca_pkey;
       public            postgres    false    298    298            �           2606    65951    usuario usuario_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.usuario DROP CONSTRAINT usuario_pkey;
       public            postgres    false    297            �           2606    65953    usuario_rol usuario_rol_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.usuario_rol
    ADD CONSTRAINT usuario_rol_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.usuario_rol DROP CONSTRAINT usuario_rol_pkey;
       public            postgres    false    300            �           2606    65955 D   variedad_arroz_etapa_fenologica variedad_arroz_etapa_fenologica_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.variedad_arroz_etapa_fenologica
    ADD CONSTRAINT variedad_arroz_etapa_fenologica_pkey PRIMARY KEY (id);
 n   ALTER TABLE ONLY public.variedad_arroz_etapa_fenologica DROP CONSTRAINT variedad_arroz_etapa_fenologica_pkey;
       public            postgres    false    303            �           2606    65957 "   variedad_arroz variedad_arroz_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.variedad_arroz
    ADD CONSTRAINT variedad_arroz_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.variedad_arroz DROP CONSTRAINT variedad_arroz_pkey;
       public            postgres    false    302            x           1259    65960    ix_password_resets_email    INDEX     U   CREATE INDEX ix_password_resets_email ON public.password_resets USING btree (email);
 ,   DROP INDEX public.ix_password_resets_email;
       public            postgres    false    269            y           1259    65961    ix_password_resets_id    INDEX     O   CREATE INDEX ix_password_resets_id ON public.password_resets USING btree (id);
 )   DROP INDEX public.ix_password_resets_id;
       public            postgres    false    269            z           1259    65962    ix_password_resets_token    INDEX     \   CREATE UNIQUE INDEX ix_password_resets_token ON public.password_resets USING btree (token);
 ,   DROP INDEX public.ix_password_resets_token;
       public            postgres    false    269            �           2620    65963    cultivo before_insert_cultivo    TRIGGER     ~   CREATE TRIGGER before_insert_cultivo BEFORE INSERT ON public.cultivo FOR EACH ROW EXECUTE FUNCTION public.set_slug_cultivo();
 6   DROP TRIGGER before_insert_cultivo ON public.cultivo;
       public          postgres    false    229    309            �           2620    65964    finca before_insert_finca    TRIGGER     x   CREATE TRIGGER before_insert_finca BEFORE INSERT ON public.finca FOR EACH ROW EXECUTE FUNCTION public.set_slug_finca();
 2   DROP TRIGGER before_insert_finca ON public.finca;
       public          postgres    false    310    237            �           2620    65965    lote before_insert_lote    TRIGGER     u   CREATE TRIGGER before_insert_lote BEFORE INSERT ON public.lote FOR EACH ROW EXECUTE FUNCTION public.set_slug_lote();
 0   DROP TRIGGER before_insert_lote ON public.lote;
       public          postgres    false    311    249            �           2620    65966 "   analisis_edafologico set_timestamp    TRIGGER     �   CREATE TRIGGER set_timestamp BEFORE UPDATE ON public.analisis_edafologico FOR EACH ROW EXECUTE FUNCTION public.update_timestamp();
 ;   DROP TRIGGER set_timestamp ON public.analisis_edafologico;
       public          postgres    false    217    313            �           2620    65967 +   analisis_edafologico trigger_actualizado_en    TRIGGER     �   CREATE TRIGGER trigger_actualizado_en BEFORE UPDATE ON public.analisis_edafologico FOR EACH ROW EXECUTE FUNCTION public.update_actualizado_en();
 D   DROP TRIGGER trigger_actualizado_en ON public.analisis_edafologico;
       public          postgres    false    312    217            �           2606    65968 6   analisis_edafologico analisis_edafologico_lote_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.analisis_edafologico
    ADD CONSTRAINT analisis_edafologico_lote_id_fkey FOREIGN KEY (lote_id) REFERENCES public.lote(id);
 `   ALTER TABLE ONLY public.analisis_edafologico DROP CONSTRAINT analisis_edafologico_lote_id_fkey;
       public          postgres    false    249    217    4963            �           2606    65973 <   analisis_edafologico analisis_edafologico_tipo_suelo_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.analisis_edafologico
    ADD CONSTRAINT analisis_edafologico_tipo_suelo_id_fkey FOREIGN KEY (tipo_suelo_id) REFERENCES public.tipo_suelo(id);
 f   ALTER TABLE ONLY public.analisis_edafologico DROP CONSTRAINT analisis_edafologico_tipo_suelo_id_fkey;
       public          postgres    false    217    5010    288            �           2606    65978    cosecha cosecha_cultivo_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.cosecha
    ADD CONSTRAINT cosecha_cultivo_id_fkey FOREIGN KEY (cultivo_id) REFERENCES public.cultivo(id) ON DELETE CASCADE;
 I   ALTER TABLE ONLY public.cosecha DROP CONSTRAINT cosecha_cultivo_id_fkey;
       public          postgres    false    229    221    4943            �           2606    65983 5   costos_estimados costos_estimados_tarea_labor_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.costos_estimados
    ADD CONSTRAINT costos_estimados_tarea_labor_id_fkey FOREIGN KEY (tarea_labor_id) REFERENCES public.tarea_labor_cultural(id);
 _   ALTER TABLE ONLY public.costos_estimados DROP CONSTRAINT costos_estimados_tarea_labor_id_fkey;
       public          postgres    false    5002    225    282            �           2606    65988 /   costos_reales costos_reales_tarea_labor_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.costos_reales
    ADD CONSTRAINT costos_reales_tarea_labor_id_fkey FOREIGN KEY (tarea_labor_id) REFERENCES public.tarea_labor_cultural(id);
 Y   ALTER TABLE ONLY public.costos_reales DROP CONSTRAINT costos_reales_tarea_labor_id_fkey;
       public          postgres    false    282    227    5002            �           2606    65993    cultivo cultivo_lote_id_fkey    FK CONSTRAINT     z   ALTER TABLE ONLY public.cultivo
    ADD CONSTRAINT cultivo_lote_id_fkey FOREIGN KEY (lote_id) REFERENCES public.lote(id);
 F   ALTER TABLE ONLY public.cultivo DROP CONSTRAINT cultivo_lote_id_fkey;
       public          postgres    false    4963    229    249            �           2606    65998     cultivo cultivo_variedad_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.cultivo
    ADD CONSTRAINT cultivo_variedad_id_fkey FOREIGN KEY (variedad_id) REFERENCES public.variedad_arroz(id);
 J   ALTER TABLE ONLY public.cultivo DROP CONSTRAINT cultivo_variedad_id_fkey;
       public          postgres    false    302    5030    229            �           2606    66003 C   diagnostico_fitosanitario diagnostico_fitosanitario_cultivo_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.diagnostico_fitosanitario
    ADD CONSTRAINT diagnostico_fitosanitario_cultivo_id_fkey FOREIGN KEY (cultivo_id) REFERENCES public.cultivo(id);
 m   ALTER TABLE ONLY public.diagnostico_fitosanitario DROP CONSTRAINT diagnostico_fitosanitario_cultivo_id_fkey;
       public          postgres    false    229    4943    231            �           2606    66008    gastos fk_cultivo_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.gastos
    ADD CONSTRAINT fk_cultivo_id FOREIGN KEY (cultivo_id) REFERENCES public.cultivo(id) ON DELETE CASCADE;
 >   ALTER TABLE ONLY public.gastos DROP CONSTRAINT fk_cultivo_id;
       public          postgres    false    239    4943    229            �           2606    66013 3   variedad_arroz_etapa_fenologica fk_etapa_fenologica    FK CONSTRAINT     �   ALTER TABLE ONLY public.variedad_arroz_etapa_fenologica
    ADD CONSTRAINT fk_etapa_fenologica FOREIGN KEY (etapa_fenologica_id) REFERENCES public.etapa_fenologica(id);
 ]   ALTER TABLE ONLY public.variedad_arroz_etapa_fenologica DROP CONSTRAINT fk_etapa_fenologica;
       public          postgres    false    4949    235    303            �           2606    66018 '   tarea_labor_cultural fk_insumo_agricola    FK CONSTRAINT     �   ALTER TABLE ONLY public.tarea_labor_cultural
    ADD CONSTRAINT fk_insumo_agricola FOREIGN KEY (insumo_agricola_id) REFERENCES public.insumo_agricola(id);
 Q   ALTER TABLE ONLY public.tarea_labor_cultural DROP CONSTRAINT fk_insumo_agricola;
       public          postgres    false    282    4959    245            �           2606    66023 *   insumo_agricola fk_insumo_agricola_cultivo    FK CONSTRAINT     �   ALTER TABLE ONLY public.insumo_agricola
    ADD CONSTRAINT fk_insumo_agricola_cultivo FOREIGN KEY (cultivo_id) REFERENCES public.cultivo(id);
 T   ALTER TABLE ONLY public.insumo_agricola DROP CONSTRAINT fk_insumo_agricola_cultivo;
       public          postgres    false    229    245    4943            �           2606    66028 &   tarea_labor_cultural fk_labor_cultural    FK CONSTRAINT     �   ALTER TABLE ONLY public.tarea_labor_cultural
    ADD CONSTRAINT fk_labor_cultural FOREIGN KEY (labor_cultural_id) REFERENCES public.labor_cultural(id);
 P   ALTER TABLE ONLY public.tarea_labor_cultural DROP CONSTRAINT fk_labor_cultural;
       public          postgres    false    247    4961    282            �           2606    66033 +   tarea_labor_cultural fk_maquinaria_agricola    FK CONSTRAINT     �   ALTER TABLE ONLY public.tarea_labor_cultural
    ADD CONSTRAINT fk_maquinaria_agricola FOREIGN KEY (maquinaria_agricola_id) REFERENCES public.maquinaria_agricola(id);
 U   ALTER TABLE ONLY public.tarea_labor_cultural DROP CONSTRAINT fk_maquinaria_agricola;
       public          postgres    false    282    255    4969            �           2606    66038 "   analisis_edafologico fk_tipo_suelo    FK CONSTRAINT     �   ALTER TABLE ONLY public.analisis_edafologico
    ADD CONSTRAINT fk_tipo_suelo FOREIGN KEY (tipo_suelo_id) REFERENCES public.tipo_suelo(id);
 L   ALTER TABLE ONLY public.analisis_edafologico DROP CONSTRAINT fk_tipo_suelo;
       public          postgres    false    288    5010    217            �           2606    66043    insumo_agricola fk_unidad_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.insumo_agricola
    ADD CONSTRAINT fk_unidad_id FOREIGN KEY (unidad_id) REFERENCES public.unidad_insumo(id);
 F   ALTER TABLE ONLY public.insumo_agricola DROP CONSTRAINT fk_unidad_id;
       public          postgres    false    245    5016    293            �           2606    66048    tarea_labor_cultural fk_usuario    FK CONSTRAINT     �   ALTER TABLE ONLY public.tarea_labor_cultural
    ADD CONSTRAINT fk_usuario FOREIGN KEY (usuario_id) REFERENCES public.usuario(id);
 I   ALTER TABLE ONLY public.tarea_labor_cultural DROP CONSTRAINT fk_usuario;
       public          postgres    false    297    5024    282            �           2606    66053 1   variedad_arroz_etapa_fenologica fk_variedad_arroz    FK CONSTRAINT     �   ALTER TABLE ONLY public.variedad_arroz_etapa_fenologica
    ADD CONSTRAINT fk_variedad_arroz FOREIGN KEY (variedad_arroz_id) REFERENCES public.variedad_arroz(id);
 [   ALTER TABLE ONLY public.variedad_arroz_etapa_fenologica DROP CONSTRAINT fk_variedad_arroz;
       public          postgres    false    303    5030    302            �           2606    66058 1   variedad_arroz fk_variedad_arroz_etapa_fenologica    FK CONSTRAINT     �   ALTER TABLE ONLY public.variedad_arroz
    ADD CONSTRAINT fk_variedad_arroz_etapa_fenologica FOREIGN KEY (variedad_arroz_etapa_fenologica_id) REFERENCES public.variedad_arroz_etapa_fenologica(id);
 [   ALTER TABLE ONLY public.variedad_arroz DROP CONSTRAINT fk_variedad_arroz_etapa_fenologica;
       public          postgres    false    302    5032    303            �           2606    66063    gastos gastos_lote_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.gastos
    ADD CONSTRAINT gastos_lote_id_fkey FOREIGN KEY (cultivo_id) REFERENCES public.lote(id) ON DELETE CASCADE;
 D   ALTER TABLE ONLY public.gastos DROP CONSTRAINT gastos_lote_id_fkey;
       public          postgres    false    249    4963    239            �           2606    66068 .   gastos_variables gastos_variables_id_agua_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.gastos_variables
    ADD CONSTRAINT gastos_variables_id_agua_fkey FOREIGN KEY (id_agua) REFERENCES public.agua(id);
 X   ALTER TABLE ONLY public.gastos_variables DROP CONSTRAINT gastos_variables_id_agua_fkey;
       public          postgres    false    4925    215    243            �           2606    66073 <   gastos_variables gastos_variables_id_costos_adicionales_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.gastos_variables
    ADD CONSTRAINT gastos_variables_id_costos_adicionales_fkey FOREIGN KEY (id_costos_adicionales) REFERENCES public.costos_adicionales(id);
 f   ALTER TABLE ONLY public.gastos_variables DROP CONSTRAINT gastos_variables_id_costos_adicionales_fkey;
       public          postgres    false    243    4933    223            �           2606    66078 L   gastos_variables gastos_variables_id_gastos_administrativos_financieros_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.gastos_variables
    ADD CONSTRAINT gastos_variables_id_gastos_administrativos_financieros_fkey FOREIGN KEY (id_gastos_administrativos_financieros) REFERENCES public.gastos_administrativos_financieros(id);
 v   ALTER TABLE ONLY public.gastos_variables DROP CONSTRAINT gastos_variables_id_gastos_administrativos_financieros_fkey;
       public          postgres    false    4955    243    240            �           2606    66083 3   insumo_agricola insumo_agricola_tipo_insumo_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.insumo_agricola
    ADD CONSTRAINT insumo_agricola_tipo_insumo_id_fkey FOREIGN KEY (tipo_insumo_id) REFERENCES public.tipo_insumo(id);
 ]   ALTER TABLE ONLY public.insumo_agricola DROP CONSTRAINT insumo_agricola_tipo_insumo_id_fkey;
       public          postgres    false    5008    286    245            �           2606    66088 6   labor_cultural labor_cultural_id_etapa_fenologica_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.labor_cultural
    ADD CONSTRAINT labor_cultural_id_etapa_fenologica_fkey FOREIGN KEY (id_etapa_fenologica) REFERENCES public.etapa_fenologica(id);
 `   ALTER TABLE ONLY public.labor_cultural DROP CONSTRAINT labor_cultural_id_etapa_fenologica_fkey;
       public          postgres    false    247    235    4949            �           2606    66093    lote lote_finca_id_fkey    FK CONSTRAINT     w   ALTER TABLE ONLY public.lote
    ADD CONSTRAINT lote_finca_id_fkey FOREIGN KEY (finca_id) REFERENCES public.finca(id);
 A   ALTER TABLE ONLY public.lote DROP CONSTRAINT lote_finca_id_fkey;
       public          postgres    false    237    4951    249            �           2606    66098 7   macronutriente macronutriente_parametro_quimico_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.macronutriente
    ADD CONSTRAINT macronutriente_parametro_quimico_id_fkey FOREIGN KEY (parametro_quimico_id) REFERENCES public.parametro_quimico(id);
 a   ALTER TABLE ONLY public.macronutriente DROP CONSTRAINT macronutriente_parametro_quimico_id_fkey;
       public          postgres    false    4983    267    251            �           2606    66103 7   micronutriente micronutriente_parametro_quimico_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.micronutriente
    ADD CONSTRAINT micronutriente_parametro_quimico_id_fkey FOREIGN KEY (parametro_quimico_id) REFERENCES public.parametro_quimico(id);
 a   ALTER TABLE ONLY public.micronutriente DROP CONSTRAINT micronutriente_parametro_quimico_id_fkey;
       public          postgres    false    267    257    4983            �           2606    66108 =   monitoreos monitoreos_variedad_arroz_etapa_fenologica_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.monitoreos
    ADD CONSTRAINT monitoreos_variedad_arroz_etapa_fenologica_id_fkey FOREIGN KEY (variedad_arroz_etapa_fenologica_id) REFERENCES public.variedad_arroz_etapa_fenologica(id);
 g   ALTER TABLE ONLY public.monitoreos DROP CONSTRAINT monitoreos_variedad_arroz_etapa_fenologica_id_fkey;
       public          postgres    false    5032    303    259            �           2606    66113 @   operacion_mecanizacion operacion_mecanizacion_maquinaria_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.operacion_mecanizacion
    ADD CONSTRAINT operacion_mecanizacion_maquinaria_id_fkey FOREIGN KEY (maquinaria_id) REFERENCES public.maquinaria_agricola(id);
 j   ALTER TABLE ONLY public.operacion_mecanizacion DROP CONSTRAINT operacion_mecanizacion_maquinaria_id_fkey;
       public          postgres    false    255    4969    261            �           2606    66118 A   operacion_mecanizacion operacion_mecanizacion_tarea_labor_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.operacion_mecanizacion
    ADD CONSTRAINT operacion_mecanizacion_tarea_labor_id_fkey FOREIGN KEY (tarea_labor_id) REFERENCES public.tarea_labor_cultural(id);
 k   ALTER TABLE ONLY public.operacion_mecanizacion DROP CONSTRAINT operacion_mecanizacion_tarea_labor_id_fkey;
       public          postgres    false    261    5002    282            �           2606    66123 D   parametro_biologico parametro_biologico_analisis_edafologico_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.parametro_biologico
    ADD CONSTRAINT parametro_biologico_analisis_edafologico_id_fkey FOREIGN KEY (analisis_edafologico_id) REFERENCES public.analisis_edafologico(id);
 n   ALTER TABLE ONLY public.parametro_biologico DROP CONSTRAINT parametro_biologico_analisis_edafologico_id_fkey;
       public          postgres    false    263    217    4927            �           2606    66128 >   parametro_fisico parametro_fisico_analisis_edafologico_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.parametro_fisico
    ADD CONSTRAINT parametro_fisico_analisis_edafologico_id_fkey FOREIGN KEY (analisis_edafologico_id) REFERENCES public.analisis_edafologico(id);
 h   ALTER TABLE ONLY public.parametro_fisico DROP CONSTRAINT parametro_fisico_analisis_edafologico_id_fkey;
       public          postgres    false    265    217    4927            �           2606    66133 /   parametro_fisico parametro_fisico_color_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.parametro_fisico
    ADD CONSTRAINT parametro_fisico_color_id_fkey FOREIGN KEY (color_id) REFERENCES public.color(id);
 Y   ALTER TABLE ONLY public.parametro_fisico DROP CONSTRAINT parametro_fisico_color_id_fkey;
       public          postgres    false    265    219    4929            �           2606    66138 1   parametro_fisico parametro_fisico_textura_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.parametro_fisico
    ADD CONSTRAINT parametro_fisico_textura_id_fkey FOREIGN KEY (textura_id) REFERENCES public.textura(id);
 [   ALTER TABLE ONLY public.parametro_fisico DROP CONSTRAINT parametro_fisico_textura_id_fkey;
       public          postgres    false    5004    265    284            �           2606    66143 @   parametro_quimico parametro_quimico_analisis_edafologico_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.parametro_quimico
    ADD CONSTRAINT parametro_quimico_analisis_edafologico_id_fkey FOREIGN KEY (analisis_edafologico_id) REFERENCES public.analisis_edafologico(id);
 j   ALTER TABLE ONLY public.parametro_quimico DROP CONSTRAINT parametro_quimico_analisis_edafologico_id_fkey;
       public          postgres    false    4927    267    217            �           2606    66148 <   phenological_stages phenological_stages_rice_variety_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.phenological_stages
    ADD CONSTRAINT phenological_stages_rice_variety_id_fkey FOREIGN KEY (rice_variety_id) REFERENCES public.rice_varieties(id);
 f   ALTER TABLE ONLY public.phenological_stages DROP CONSTRAINT phenological_stages_rice_variety_id_fkey;
       public          postgres    false    273    4996    277            �           2606    66153 :   registro_meteorologico registro_meteorologico_lote_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.registro_meteorologico
    ADD CONSTRAINT registro_meteorologico_lote_id_fkey FOREIGN KEY (lote_id) REFERENCES public.lote(id);
 d   ALTER TABLE ONLY public.registro_meteorologico DROP CONSTRAINT registro_meteorologico_lote_id_fkey;
       public          postgres    false    275    249    4963            �           2606    66158 '   rol_permiso rol_permiso_permiso_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.rol_permiso
    ADD CONSTRAINT rol_permiso_permiso_id_fkey FOREIGN KEY (permiso_id) REFERENCES public.permiso(id);
 Q   ALTER TABLE ONLY public.rol_permiso DROP CONSTRAINT rol_permiso_permiso_id_fkey;
       public          postgres    false    4990    281    271            �           2606    66163 #   rol_permiso rol_permiso_rol_id_fkey    FK CONSTRAINT        ALTER TABLE ONLY public.rol_permiso
    ADD CONSTRAINT rol_permiso_rol_id_fkey FOREIGN KEY (rol_id) REFERENCES public.rol(id);
 M   ALTER TABLE ONLY public.rol_permiso DROP CONSTRAINT rol_permiso_rol_id_fkey;
       public          postgres    false    281    4998    279            �           2606    66168 9   tarea_labor_cultural tarea_labor_cultural_cultivo_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tarea_labor_cultural
    ADD CONSTRAINT tarea_labor_cultural_cultivo_id_fkey FOREIGN KEY (cultivo_id) REFERENCES public.cultivo(id);
 c   ALTER TABLE ONLY public.tarea_labor_cultural DROP CONSTRAINT tarea_labor_cultural_cultivo_id_fkey;
       public          postgres    false    229    4943    282            �           2606    66173 8   tarea_labor_cultural tarea_labor_cultural_estado_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tarea_labor_cultural
    ADD CONSTRAINT tarea_labor_cultural_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES public.estado(id);
 b   ALTER TABLE ONLY public.tarea_labor_cultural DROP CONSTRAINT tarea_labor_cultural_estado_id_fkey;
       public          postgres    false    4947    233    282            �           2606    66178 8   tarea_labor_cultural tarea_labor_cultural_insumo_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tarea_labor_cultural
    ADD CONSTRAINT tarea_labor_cultural_insumo_id_fkey FOREIGN KEY (insumo_agricola_id) REFERENCES public.insumo_agricola(id);
 b   ALTER TABLE ONLY public.tarea_labor_cultural DROP CONSTRAINT tarea_labor_cultural_insumo_id_fkey;
       public          postgres    false    282    4959    245            �           2606    66183 7   tarea_labor_cultural tarea_labor_cultural_labor_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tarea_labor_cultural
    ADD CONSTRAINT tarea_labor_cultural_labor_id_fkey FOREIGN KEY (labor_cultural_id) REFERENCES public.labor_cultural(id);
 a   ALTER TABLE ONLY public.tarea_labor_cultural DROP CONSTRAINT tarea_labor_cultural_labor_id_fkey;
       public          postgres    false    282    247    4961            �           2606    66188 !   usuario_rol usuario_rol_rol_id_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.usuario_rol
    ADD CONSTRAINT usuario_rol_rol_id_fk FOREIGN KEY (rol_id) REFERENCES public.rol(id) NOT VALID;
 K   ALTER TABLE ONLY public.usuario_rol DROP CONSTRAINT usuario_rol_rol_id_fk;
       public          postgres    false    300    4998    279            �           2606    66193 %   usuario_rol usuario_rol_usuario_id_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.usuario_rol
    ADD CONSTRAINT usuario_rol_usuario_id_fk FOREIGN KEY (usuario_id) REFERENCES public.usuario(id) ON DELETE CASCADE;
 O   ALTER TABLE ONLY public.usuario_rol DROP CONSTRAINT usuario_rol_usuario_id_fk;
       public          postgres    false    297    5024    300            �           2606    66198 P   variedad_arroz_etapa_fenologica variedad_arroz_etapa_fenologica_variedad_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.variedad_arroz_etapa_fenologica
    ADD CONSTRAINT variedad_arroz_etapa_fenologica_variedad_id_fkey FOREIGN KEY (variedad_arroz_id) REFERENCES public.variedad_arroz(id);
 z   ALTER TABLE ONLY public.variedad_arroz_etapa_fenologica DROP CONSTRAINT variedad_arroz_etapa_fenologica_variedad_id_fkey;
       public          postgres    false    5030    303    302            n      x������ � �      p   i   x�}���@�s4��-q\Tp����c>y"��@#y�b���f�����Ln��,�knyp�\�A>^'c�%U���=G�4c��6��`7�`��%�QE��%�      �      x������ � �      r      x�3��������� +�      t   9   x���  ����ւ(�����iP��y�(��A:�3�/D����UD.i	�      v      x������ � �      x      x������ � �      z      x������ � �      |   U   x�3�t.�)�,�WP6�A##]#]#(�L�В3�Hא����A�u����pF\&�@�&U��L�c�=... ��"�      ~   �   x���M
�0�����}��4팇�IbZ�����Fp��-_���I�����[�|�s�!hF%�V��	Y�`)H��<w�uF�[��y����^����&�?8��%S��:�<�dQ�6feV���?:��[_<�      �   6   x�3�H�K�L�+I���2�t�S((�ON-��9��srRKS��=... �[      �   D   x�3�t-I,HTKMO-I,�,K�4�2�
�委&����&P�T�ĔҢ���Û�1z\\\ �oe      �   �   x�E̱
�0����}�sIz:wq���r����)	��M3�o��??7�9.��3��>@CD�M�` D��?c���aH��)�r�*�}���pw�!�����Nџ�o^9gx&����R���*�      �   �   x�]��
�0Eg�+�%���1t�ڬ]�-� �����$�B�x.�\���m/����� �K����ۛ	�� ��9��pTJ��Y4a2!�j�����#�o�m��Lsf�w��AS��*�y�D���2.��_��i�I�;��s��v=�      �      x������ � �      �      x������ � �      �   �   x�u�Mj�0���S�A)r���.͢�e#\j��
�9}�Pp]��|�<��.S�0;�5�޴�8�~����0������,nO5Y
`����a_dǔ���?�h���!9�%+��n�6Cs��<c�)�"Cl����/��w-ک�z�j��Լe��:[��>\
�U���!Ǐx�2��I����V/0���p��Kb�!�oU5Z      �   |   x�3�tNLJ�����LLI���44 =ǈ˘ӱ '39193?O!%U�#�()39��E�	gpfjnR�9s4c����1�0�tLIM.�;��0G�$��(5/$m��?�=... �a3�      �   O   x�3���/IUP6�B�����������eUiTidld����*4�*4�4�4B21�4�$�,_Ii� � �      �      x������ � �      �      x������ � �      �   1   x�3�)JL.�/R����SpIM-JU05�4H��4600�������� ��
[      �      x������ � �      �   q   x�3��M�I�J,�4�v"NCN##]CC]#C�?NC.3΀��t���ĔҢ����<du�uFpÌ8s�UX@T�r�楥妦$�����D���t��f@�1z\\\ w^%      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �   c  x���I��0�uq�� ��Yu
2�SB��H @�4I�N�Բr��l�Y����]T�n��;�I�����UQ~��z;��s�Nr;��ɀ,7nF툉fHFy��-�L�?~�Ki���9T��;dy�d��
��]�l=�w������6L�%�x�PN�����(�� �Fb��a5�� "<�<R~AYEXET�(�D���|��y��t�
iڜ�(�b4n,����^���ީ������W�q� �� �d�0����&k���չ+�W�R�(nV�mc�AV�'p�ZZ����=��'��UI�X"y�֗	�
k�Bs�fn�3Y�렺F�V��=۴I=����ḧ����y�*�	�P�8�u �� �-G�p� P���>h���i�Ƌ;2QYWN��(���nI�{PH��
'���C̊���#�ι`3x��.̇�*h(	¬r�?T{��0�kbџ(* *��X�PD��" `��;7��{o>�����%��N��8�=4�24HK��=����-�̌� U1U�(B1@��:�n��̛ד���9��]$�ѡ]/� �CB�۵��P�٣7�s�x�B*�"E2��
���e�      �   ,  x�u�K��0D�p�Q��%�-!�(ģ$�bN?���d��ʎM�D5	�_�
Fa����
�¬~9�*9�EiN����~�����1�glz+=�ĥ�Hz����|�?l|+Y��A%�8k��_���I8��/�|yQ��M�U��X��7YP+�F�e�Ï��Ig2���A\����I?�	o���)�`Ɠţ�I�u釚���2pPIZ��$7����l��mnCDN%���
�S=�����$�"�Y2&�g���u�R��9cN3�#Ns!9z���r�wL�/�e��bIC���U��	uy      �      x������ � �      �   �  x���o�0ǟ����3�|�����M^c6�$��tP�����-��iS��"W���|���Sd�2�X2�1Ad@AJ3mp��"��6!������Km�/V�uW�b_��6�/�$Lj�fQ�n�#Zku�_�n|���"`��׸����z���"*��W]�!�,����j��B�j�����+��<8�KA��������������e��QL�b�e��F�};�6���m��hWTn�M�°��6q�{wY�[_����jҌ���m��U��D���v4��x_%��J�\�(fޛ�a�Ɗ"���3C%5�k����&���%ۥ�Xg�m�n���v�۶�E,�m잎r��\ H<o���n1|	f�?��JSe���5�|��sE:3��w�-&��1X�ѩ�T�9:���K&���)qvt��ѩQ�TO�T��S�S�	D��Nx-��PqNtNXIVAΏ�S�T��	���<��8�D<���x:ҩ�`Z�t��tjj���b��X\��W:�!��Wk\�ڸv����^O
�8�-�V������s]2��0������{�m���8�8���?���F�p�p�N�D)m����p
�C�(.��3�3�'��R�Ɵ�F��x:YI�4���<��*G�5&� y�� �,�g      �      x������ � �      �   M   x�3�tL����,.)JL�/��2��tDPHIUp��KN��27�tL/�����r9R����s@J�s��1z\\\ \�/      �   �   x�%���� �&�+4�����q�ᡮ�eZ9��dWu�]�kw}]1�P�u�ʿ�س�}��o#��{�>��L�8Ę#�C���	C�H���1#1#1#1�0
�0�o.����}1���o�O�&�9�;�Igz���r�ۋ�����\�6?�.{�޴�ʮ�ʮ�ʮ��n�M�y��ݴ�v�n�/�L9Sά��c�S�MV      �   �   x�U��!ߦ"{m��Tp�T��@x0B32J`XfdA��MJ_��;��y�U+���W����.quvv��"WD���]��#)�]���5��W>��j�*̪��j�F\U�S�0��zv�[2׈!k3�Ô�
DU����y��~�`T�      �      x�3�t,J��/N����� !��      �   :   x�3�N����I�2��H-J�L�LI�2�tK-*��ɬJ�+I�2�t+�K�H��qqq ӧ|      �   '   x�3�.M��WH,J��/��2����3sr@"1z\\\ ��!      �      x��ZɎ�ضW}E� ͦ�l��ѓ`��6�i���uK��9vށ3�Y�P�V�ko��<�Y�Or5{%:�j�	+By�V�7럪��Ղ��\T�G��_�� ~���H&�
o��H�e�˕��N
���U�3T6���"�����f���T�2r�4�^�Oe�z�|e����L�Rp�����(�B�_��Jlh%`�O�=E`���z&v�SD�O7X�z�آqA���
�"�����imp�~�A��hb!����%�+G�i+`9P	�g��B�9��"��"���`$A���J����~"V���7k�BP����@����-]�*N�^��Yᒟ���`)�Af�t'��V��%�ؼo�ޝ��\��"�_����5���"
ǌ�"�
'<��6Q����4��O�x^6"2�*_ńy�D� Ju�Y`���|�,�y� ��p��p�2����+$t8�kq��"(��~ �E7$��ER\��'b����$�,���ޅ���Ԝ����;��N'���Y��cJ58���{�=��H8�G�.�?��WY��>���@�� ���OS�Z��H�ŌGds�c*5e���d�fc�;�9�(���1.��=���p��F>b���J���:�;u��qn��y3}�0�!��&
���� ��L}��X¯����Q��M��fqaQC��P@��V �:>�2���7�K�V�L�o��F��S�L6-��1B��e��΅������4x�MVf��%O%|���z��n�H-:�^g�n?�٘n��󕃧�)˟���}T/����'��s%l1��z����u��������ě'�JlY�R�O�:�c1�l�rt���ƂkMIdؾ:�s�4�!:��{�|	�NGgIu#�jx�8�����6+g��R�H"��_�O7�ש����������`��L}����#��8ƈA�(��Sg^)iъ�t�r������,�@E�X��73r��L�p��<t����%7�ߊ�'�~`��E�WdI1�z.޶3̄�)#$��8*Bӻ��7L�`G��{�������rY]��lȃQ�@���LHG��[�v_�y�M��>rC�0��+�,�,/�_
�Z66�c'r�*�f�KOclﲁDq�>oő�V�~8ЋH�0u�M\�C���s3��T���OL�H���߂P��� ��4 &��O^˫�q:S���� -T�_.&IR���c�����!���4�(~���+z�d�W��YH�$��Hc`��3�>�'G58�~d=~�uJ�)��Q-�V�<�[qy!��l:�YSΒ ���(�p�V;��c���g�Y�\�}{�v܍0��ʹ���xLX@Fq�[�y�
��ȧ�8�A0��W�H�f�p��X'�9)��L�fw3&��o�5!s��*B]�6c�[o�͗�|�s�ndx�t������q��n��x�Nn�Z>�³(�gF
E�%� �_>�?� �'�h��H��B7����a7]�&v��X�d�����+rF�ح'�T.��8Ň2s.`��@��)9�I�o�`0���Q��(��kW�C�V�Ke1�*�Fqs����b�і�Ns�{��������|�;Ag��ӌ�k+yx��g��w(�U3y�oCA)�¨o�2+��L���]���KL˘\�j��sz���Э��8D���0�R3���5�@}+�ܟ���gRI����.����Ϣ�8�z
@���z.��!ev�8����J)Tx�l��Bd�D!%�1�K��{���%��$J�XC��L���@I��Ծ�L���TS����S�
��"�:Z?ۿ�0S�jX�C91��`G/yԨ�Y�O�%��QՍ�7vj���D$��&�$w�[6���(�e��A(If��O����7�E��Y�Y�s��k�9Ѷ{a�⮪X�*%kV+LQ��]Y�H�k�m��y�0���؜O�a[�S٩0c��a��1�hH�O1���n�����IC�+ʫs��n{r�ɏ��295䱱����&>9-l�@J�o��Ⱥw���B7�Y�A��J�	�:)y)�Vl���~b���ПY�D����a�"�f�pv��%`��QƔ�MF�E�C<���w�"<زb�����:ih��> Fa���#�!�O,�4D���.��{v�uf���`�t�S&k.��?�9FUC�Yz�>�r÷y�Z�@9Cqjah8W����52^�m�al�x\�%�4�k�+"�����k_�W��YgM�8�S&�+�#Y���UmϤ�l�AI�<�>��h���<�Z��~���Ӄ�ܩ�����f1΅`��ύ�Q���d��b�)v�X@����V�F�b\g��ܖ����-:�����j��f�_]h�J�����JG��zV9�CF����Su�E58���J��q����W� ���ߚbu�u��"���9���%�8;q�;��v�օ�ح��y��?�|�Ŭo3�lD��!�u���.},����%��������P���OP���kɗ�D����'B�m��pL�e�\��yߑ���}2R�Q�xB�2�L��ŏ�3�Y�p�\��yEǟ�ߊ����1|�w��$�KJK�؊撲�I�P��ޡ04o%�Q�WP79��ཅ���C�$aa�t0�Sqgr��sH47���Uƅ֏�)��E�>pr`o�q���Q��:�@+���4q#h���&��Z��q��s�]R�{{�؟&<��*�|�°��5�Lɭ��ԾC�P��k��"�g�[̈́�ޢ����X���B�ؑc��r�����v���b�DW�ۙ��2�!Wn��B��U��Z�DlE���f>�,��Ľ��F6�A�!�w�d�_�Mɶ��׀f���Dh|7��;|'���rk�����}�.2b���"��v��jfw�:��
	Ũ�^�'=�oO� �s`#I��{R�OK㯈M�n��ɩf_��yq���_Q�o���l1�ڈICޏ:/��� ̾����n�\8�S��2��m����y����9����g�_�/���+��|�BD̛;�V���^GњȄļ�P?���Skw��'��a� �f��zz��R[���|^���(�@�cƉ���3+����{5�8},�;��?sG��L�W����ו���w5�%0Y�}ޒ�2?��s�$yC@Ax?8\m�
��}���u9L�4�W&//���L� R�Wy��OT�`n���.�f�4ev�Q{��r�7>�d��I�LG1.��T��I��9InOX�{������0�-Q֬���O⥟2|w
,��*:b����!}_��'�A���{�O�@��W�)
\�Z��S���'@u%쩩�{I�W����� ��l�ȿ$�^$�{G���5:�\�(-�Cz��W2=���|}�g�ް��R<ݹ�!�t�dnOr0�q���D,�u��9���b��sX{���}����νW���Cu��I&����@E�ړ��{������K`6�.7+iz���v=q���kr�s�y\`�����s�ϛ�	���������������,�����'��[��.�"����L^o������e������0��g��!�F��N;/��c�����r/L�6��9%��o�<� �G������j<\g@�Gm(���&_ ��c�n��(�Ũ�;L1J76�0Nj,7*��x��`0��	�D��$)�������z%"�{�U�����D[�e��{�y%j�x�߀}���y�����gU��І�u�Լ�s�{��P����r0z��|g=�����ov�؎�
&��ǐ�7�ơ�D����*%�u3��G�����-`6��1��hE���AǪ��z�YᨱZg��5����������9{��gbB�Uh)(�wPF���т�,,>���ȶ&���1�ޛJ�v�=J/����Z�-!��w�����+ٳ�l���^��\��5�������?��_K#��      �      x�3��M-)������ @      �   0   x�3�����O/J���2���,)��2�t�M8C��RsS�b���� +��      �      x������ � �      �   �  x�m�Ͷ�0���)�1
� ����"� �N�"y��]8��{�s������p�
�E5��&ܽ�?P�;A\LS�%D_��U_"��H��bOةY[f�^��a,�j<5��g�N�痒d����� �3��p1TXY1
4@ڀ;��iy�J��ȗC�J�H�3�r�%0+A|����Μ���Nܜʗ���Гx�@dC%;1T �@�.䊷�DLm8vV�;7��� 9��+yϖq|8��ĮC�H��`6����	z��!�th3�>&�������	���^ʥ�v�qwO8����?�e);=0k�k��8�k���b�vЩ,�S�wL���m��8��O���L��5%fR��� ������ �S��#G8tv����*�z���H�-����>��|<��䭪Ţ��@r,�9K8��$�m7�gO�L��z�Fi����{�����W9l�	�

��ts}̕���$1\�����6��[�����*�F/l��w�u2�F�"���^=s�o��J�i�~����N�ݕ<j^}�n���4�r�Bg��\��"u��vy���"�6}�z�lpL	,���!��i�bk?13(SQ�e�x�RA׮ͨ*�5��k��y��8�|Sn�F.v5����o(K�      �   (   x�341�4�241��`�LZ�HS0i&��d� �7�      �   B   x����0��TL6���_G~;7�(�3.<�-�*Ӥ;Ғ=Z�m��|���iF��{���      �   ;   x�3���.M���ttv56����2�tKMIM,*ʯR017�4661rv46K��qqq ��      �   9   x�%�K  ��V�(�,��2���>b�2���3�2���y�s/�î�     