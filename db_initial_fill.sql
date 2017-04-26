
    --    PII Tool
    --    Initial fill for the database
    --    (c) 2017 DQ&A Media Group / NMPi London

    -- Use the correct Database
    USE pii_db;

    -- Start with a clear conscience
    DELETE FROM users_client_domains;
    DELETE FROM users_schedules;
    DELETE FROM users;
    DELETE FROM schedules;
    DELETE FROM providers;
    DELETE FROM frequencies;
    DELETE FROM user_types;
    DELETE FROM client_domains;

    -- UserTypes
    INSERT INTO user_types(user_types_id, user_type) VALUES(1, 'nmpi_user');
    INSERT INTO user_types(user_types_id, user_type) VALUES(2, 'client');

    -- Frequencies
    INSERT INTO frequencies(frequencies_id, frequency, active) VALUES(1, 'daily', 1);
    INSERT INTO frequencies(frequencies_id, frequency, active) VALUES(2, 'weekly', 1);
    INSERT INTO frequencies(frequencies_id, frequency, active) VALUES(3, 'monthly', 1);
    INSERT INTO frequencies(frequencies_id, frequency, active) VALUES(4, 'yearly', 1);

    -- Users
    INSERT INTO users(users_id,email, first_name, last_name, date_added, access_token, pii_token,
            pii_token_expires, oauth_token, user_types_id, approved, active)
       VALUES(1, 'richard@dqna.com', 'Richard', 'The Doctor', now(), '', '',
            '19700101', '', 2, 1, 1);
    INSERT INTO users(users_id, email, first_name, last_name, date_added, access_token, pii_token,
            pii_token_expires, oauth_token, user_types_id, approved, active)
       VALUES(2, 'kanan@nmpi.com', 'Kanan', 'F', now(), '', '',
            '19700101', '', 1, 1, 1);
    INSERT INTO users(users_id, email, first_name, last_name, date_added, access_token, pii_token,
            pii_token_expires, oauth_token, user_types_id, approved, active)
       VALUES(3, 'paul@nmpi.com', 'Paul', 'R', now(), '', '',
            '19700101', '', 2, 1, 1);

    -- client_domains
    INSERT INTO client_domains(client_domains_id, client_domain, active) VALUES(1, 'DQ&A', 1);
    INSERT INTO client_domains(client_domains_id, client_domain, active) VALUES(2, 'NMPi', 1);

    -- user_client_domains
    INSERT INTO users_client_domains(users_id, client_domains_id) VALUES(1, 1);
    INSERT INTO users_client_domains(users_id, client_domains_id) VALUES(3, 2);

    -- Providers
    INSERT INTO providers(providers_id, provider, active) VALUES(1, 'FaceBook', 1);
    INSERT INTO providers(providers_id, provider, active) VALUES(2, 'Google', 1);

    -- Schedules
    INSERT INTO schedules(schedules_id, providers_id, frequencies_id, client_domain_id, active, hash, expires)
        VALUES(1, 1, 1, 1, 1, '', '19700101');
    INSERT INTO schedules(schedules_id, providers_id, frequencies_id, client_domain_id, active, hash, expires)
        VALUES(2, 1, 3, 1, 1, '', '19700101');
    INSERT INTO schedules(schedules_id, providers_id, frequencies_id, client_domain_id, active, hash, expires)
        VALUES(3, 2, 4, 1, 1, '', '19700101');
    INSERT INTO schedules(schedules_id, providers_id, frequencies_id, client_domain_id, active, hash, expires)
        VALUES(4, 2, 1, 2, 1, '', '19700101');
    INSERT INTO schedules(schedules_id, providers_id, frequencies_id, client_domain_id, active, hash, expires)
        VALUES(5, 1, 3, 2, 1, '', '19700101');
    INSERT INTO schedules(schedules_id, providers_id, frequencies_id, client_domain_id, active, hash, expires)
        VALUES(6, 2, 4, 2, 1, '', '19700101');

    -- User Schedules
    INSERT INTO users_schedules(users_id, schedules_id) VALUES (1, 1);
    INSERT INTO users_schedules(users_id, schedules_id) VALUES (1, 2);
    INSERT INTO users_schedules(users_id, schedules_id) VALUES (1, 3);
    INSERT INTO users_schedules(users_id, schedules_id) VALUES (3, 4);
    INSERT INTO users_schedules(users_id, schedules_id) VALUES (3, 5);
    INSERT INTO users_schedules(users_id, schedules_id) VALUES (3, 6);
    INSERT INTO users_schedules(users_id, schedules_id) VALUES (2, 1);
    INSERT INTO users_schedules(users_id, schedules_id) VALUES (2, 2);
    INSERT INTO users_schedules(users_id, schedules_id) VALUES (2, 3);
    INSERT INTO users_schedules(users_id, schedules_id) VALUES (2, 4);
    INSERT INTO users_schedules(users_id, schedules_id) VALUES (2, 5);
    INSERT INTO users_schedules(users_id, schedules_id) VALUES (2, 6);



