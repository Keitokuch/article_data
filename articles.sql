CREATE TABLE articles (
    article_id      INTEGER(11)         not null,
    title           VARCHAR(2047)        not null,
    authors         VARCHAR(1023)        not null,
    abstract        TEXT                not null,
    PRIMARY KEY(article_id),
    FULLTEXT KEY(title, authors, abstract)
);
