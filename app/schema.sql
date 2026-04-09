-- Šī rinda izdzēš tabulu rezultati, ja tā jau eksistē.
DROP TABLE IF EXISTS rezultati;

-- Šī rinda izdzēš tabulu treninu_plani, ja tā jau eksistē.
DROP TABLE IF EXISTS treninu_plani;

-- Šī rinda izdzēš tabulu vingrinajumi, ja tā jau eksistē.
DROP TABLE IF EXISTS vingrinajumi;

-- Šī rinda izdzēš tabulu lietotaji, ja tā jau eksistē.
DROP TABLE IF EXISTS lietotaji;

-- Šī rinda izveido tabulu lietotaji.
CREATE TABLE lietotaji (
    -- Šī rinda izveido primāro atslēgu id.
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Šī rinda izveido unikālu lietotājvārda lauku.
    lietotajvards TEXT NOT NULL UNIQUE,

    -- Šī rinda izveido lietotāja vārda lauku.
    vards TEXT NOT NULL,

    -- Šī rinda izveido paroles hash lauku.
    parole_hash TEXT NOT NULL,

    -- Šī rinda izveido lomas lauku ar ierobežotu vērtību sarakstu.
    loma TEXT NOT NULL CHECK (loma IN ('admins', 'lietotajs')),

    -- Šī rinda izveido lietotāja izveidošanas datuma lauku.
    izveidots TEXT NOT NULL
);

-- Šī rinda izveido tabulu vingrinajumi.
CREATE TABLE vingrinajumi (
    -- Šī rinda izveido primāro atslēgu.
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Šī rinda izveido vingrinājuma nosaukuma lauku.
    nosaukums TEXT NOT NULL UNIQUE,

    -- Šī rinda izveido muskuļu grupas lauku.
    muskulu_grupa TEXT,

    -- Šī rinda izveido apraksta lauku.
    apraksts TEXT,

    -- Šī rinda izveido aktīvs karogu.
    aktivs INTEGER NOT NULL DEFAULT 1 CHECK (aktivs IN (0, 1))
);

-- Šī rinda izveido tabulu treninu_plani.
CREATE TABLE treninu_plani (
    -- Šī rinda izveido primāro atslēgu.
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Šī rinda izveido ārējo atslēgu uz lietotāju tabulu.
    lietotajs_id INTEGER NOT NULL,

    -- Šī rinda izveido ārējo atslēgu uz vingrinājumu tabulu.
    vingrinajums_id INTEGER NOT NULL,

    -- Šī rinda izveido nedēļas dienas lauku.
    nedelas_diena TEXT NOT NULL CHECK (nedelas_diena IN ('MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN')),

    -- Šī rinda izveido komplektu skaita lauku.
    komplekti INTEGER NOT NULL CHECK (komplekti > 0),

    -- Šī rinda izveido atkārtojumu lauku.
    atkartojumi INTEGER NOT NULL CHECK (atkartojumi > 0),

    -- Šī rinda izveido secības lauku izkārtojuma vajadzībām.
    seciba INTEGER NOT NULL DEFAULT 1,

    -- Šī rinda definē ārējo atslēgu uz lietotājiem.
    FOREIGN KEY (lietotajs_id) REFERENCES lietotaji(id) ON DELETE CASCADE,

    -- Šī rinda definē ārējo atslēgu uz vingrinājumiem.
    FOREIGN KEY (vingrinajums_id) REFERENCES vingrinajumi(id) ON DELETE CASCADE
);

-- Šī rinda izveido tabulu rezultati.
CREATE TABLE rezultati (
    -- Šī rinda izveido primāro atslēgu.
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Šī rinda izveido ārējo atslēgu uz lietotāju tabulu.
    lietotajs_id INTEGER NOT NULL,

    -- Šī rinda izveido ārējo atslēgu uz vingrinājumu tabulu.
    vingrinajums_id INTEGER NOT NULL,

    -- Šī rinda izveido datuma lauku.
    datums TEXT NOT NULL,

    -- Šī rinda izveido svara lauku.
    svars_kg REAL NOT NULL DEFAULT 0 CHECK (svars_kg >= 0),

    -- Šī rinda izveido atkārtojumu lauku.
    atkartojumi INTEGER NOT NULL CHECK (atkartojumi > 0),

    -- Šī rinda izveido komplektu lauku.
    komplekti INTEGER NOT NULL DEFAULT 1 CHECK (komplekti > 0),

    -- Šī rinda izveido piezīmju lauku.
    piezimes TEXT,

    -- Šī rinda definē ārējo atslēgu uz lietotājiem.
    FOREIGN KEY (lietotajs_id) REFERENCES lietotaji(id) ON DELETE CASCADE,

    -- Šī rinda definē ārējo atslēgu uz vingrinājumiem.
    FOREIGN KEY (vingrinajums_id) REFERENCES vingrinajumi(id) ON DELETE CASCADE
);
