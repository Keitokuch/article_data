CREATE TABLE article_entries (
    entry_id        INTEGER(11)         not null,
    article_id      INTEGER(11)         not null,
    link            VARCHAR(2047)        not null,
    journal_id        INTEGER(11)         not null,
    PRIMARY KEY(entry_id),
    FOREIGN KEY(article_id) REFERENCES articles(article_id),
    FOREIGN KEY(journal_id) REFERENCES jid_name(journal_id)
);

