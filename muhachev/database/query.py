from database.connect import init_db_connection, close_conn


def getQuestion(config, number_question):
    context = init_db_connection(config)

    cursor = context.cursor()
    query = "SELECT * FROM questions WHERE section = " + str(number_question)
    cursor.execute(query)
    result = cursor.fetchone()
    close_conn(context)
    return result


async def getQuestionBySection(config, number_question):
    context = init_db_connection(config)

    cursor = context.cursor()
    query = "SELECT q.text, answers.* FROM answers " + \
            "JOIN questions q on q.id = answers.questionId " + \
            "WHERE section = " + str(number_question)
    cursor.execute(query)
    result = cursor.fetchall()
    close_conn(context)
    return result