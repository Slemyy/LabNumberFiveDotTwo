def check_access(host_ip, token) -> bool:
    try:
        with connect(
                host="localhost",
                user="root",
                password="root",
                database="users"
        ) as conn:
            with conn.cursor() as cursor:
                query = "SELECT * FROM users WHERE token = %s"
                cursor.execute(query, (token,))
                result = cursor.fetchone()

                if result:
                    if result[2] is None:
                        # Проверяем наличие записи в hosts
                        query_select_host = "SELECT * FROM hosts WHERE ip = %s"
                        cursor.execute(query_select_host, (host_ip,))
                        result_host = cursor.fetchone()

                        if not result_host:
                            host_name = socket.gethostname()
                            query_insert_host = "INSERT INTO hosts (host, ip) VALUES (%s, %s)"
                            cursor.execute(query_insert_host, (host_name, host_ip))

                        # Обновляем запись в users с айди из таблицы hosts
                        query_update_user = "UPDATE users SET host_id = (SELECT id FROM hosts WHERE ip = %s) " \
                                            "WHERE id = %s"
                        cursor.execute(query_update_user, (host_ip, result[0],))
                        conn.commit()

                        return True

                    else:
                        # Проверяем наличие записи в hosts
                        query_select_host = "SELECT * FROM hosts WHERE id = %s"
                        cursor.execute(query_select_host, (result[2],))
                        result_host = cursor.fetchone()

                        if result_host[2] == host_ip:
                            return True

                        return False
                else:
                    print(f"[TitaniumSafe] No user found with '{host_ip}' or invalid token")
                    return False

    except Exception as e:
        print("[TitaniumSafe | ERROR]", e)

    return False