def count_on_quests(chapter, status):
    quests = chapter.quests
    count = 0
    for quest in quests:
        if quest.status == status:
            count += 1
    return count


def count_on_chapters(manga, status):
    chapters = manga.chapters
    count = 0
    for chapter in chapters:
        if chapter.status == status:
            count += 1
    return count


def count_on_quests_in_manga(manga, status):
    chapters = manga.chapters
    count = 0
    for chapter in chapters:
        quests = chapter.quests
        for quest in quests:
            if quest.status == status:
                count += 1
    return count