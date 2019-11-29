CREATE TABLE article_lemma (
    article_id      INTEGER(11)         not null,
    lemma_list      text                not null,
    PRIMARY KEY(article_id),
    FOREIGN KEY(article_id) REFERENCES articles(article_id)
);

