CREATE TABLE IF NOT EXISTS "Pokemon#8738" (
	"id" INTEGER,
	"pokemon_name"	TEXT NOT NULL UNIQUE,
	"image_hashes"	TEXT NOT NULL UNIQUE,
	"pokemon_name_it"	TEXT,
	"pokemon_name_es"	TEXT,
	"pokemon_name_de"	TEXT,
	"pokemon_name_fr"	TEXT,
	"pokemon_name_cn"	TEXT,
	"pokemon_name_kr"	TEXT,
	"pokemon_name_jp"	TEXT
);