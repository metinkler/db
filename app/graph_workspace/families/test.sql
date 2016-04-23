SELECT I.game1 as game1, G.thumbnail as thumbnail1, G.bgg_id as id1, I.game2 as game2, H.thumbnail as thumbnail2, H.bgg_id as id2
     FROM ( SELECT a.boardname as game1, b.boardname as game2
            FROM boardpublisher a INNER JOIN boardpublisher b 
            ON a.pubname = b.pubname
            WHERE a.boardname < b.boardname
            LIMIT 1000) as I
     INNER JOIN board G ON (G.name = I.game1)
     INNER JOIN board H ON (I.game2 = H.name);

-- SELECT a.boardname as game1, b.boardname as game2
-- FROM boardpublisher a INNER JOIN boardpublisher b
-- WHERE a.boardname < b.boardname
-- LIMIT 100;
