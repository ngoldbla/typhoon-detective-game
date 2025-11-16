import { Case, Clue, Suspect } from '@/types/game';

export const defaultCases: Case[] = [
    {
        id: 'case-001',
        title: 'The Missing Cookie Recipe',
        description: 'Mrs. Baker\'s secret cookie recipe is missing! She was going to make cookies for the school bake sale tomorrow. The recipe card was on her desk this morning, but now it\'s gone. Can you help find out who took it?',
        summary: 'Help find Mrs. Baker\'s missing cookie recipe before the bake sale tomorrow.',
        location: 'Elementary School Kitchen',
        dateTime: '2024-03-15T14:30:00',
        difficulty: 'easy',
        solved: false,
        isLLMGenerated: false
    },
    {
        id: 'case-002',
        title: 'The Lost School Trophy',
        description: 'The big gold trophy from our class is missing! We won it at the science fair last week. It was sitting on the shelf in our classroom. Now the shelf is empty. We need to find it before the school assembly on Friday.',
        summary: 'Find the missing class trophy before the school assembly.',
        location: 'Sunny Elementary School',
        dateTime: '2024-03-20T10:15:00',
        difficulty: 'medium',
        solved: false,
        isLLMGenerated: false
    },
    {
        id: 'case-003',
        title: 'The Playground Prank',
        description: 'Someone painted funny faces on the playground swings! The swings were normal yesterday. This morning, they all had silly smiley faces painted on them. The principal wants to know who did it. Nobody is in trouble, but we need to find out who the mystery artist is!',
        summary: 'Find out who painted the silly faces on the playground swings.',
        location: 'School Playground',
        dateTime: '2024-03-25T08:00:00',
        difficulty: 'medium',
        solved: false,
        isLLMGenerated: false
    }
];

export const defaultClues: Clue[] = [
    // Case 001: The Missing Cookie Recipe
    {
        id: 'clue-001-1',
        caseId: 'case-001',
        title: 'Chocolate Fingerprints',
        description: 'There are small chocolate fingerprints on the desk where the recipe was. The chocolate is still a little wet.',
        location: 'Mrs. Baker\'s Desk',
        type: 'physical',
        discovered: true,
        examined: false,
        relevance: 'critical',
        imageUrl: '/clue.png'
    },
    {
        id: 'clue-001-2',
        caseId: 'case-001',
        title: 'Open Window',
        description: 'The window next to the desk is open. There are muddy footprints on the windowsill from outside.',
        location: 'Kitchen Window',
        type: 'physical',
        discovered: true,
        examined: false,
        relevance: 'important',
        imageUrl: '/clue.png'
    },
    {
        id: 'clue-001-3',
        caseId: 'case-001',
        title: 'Sign-In Sheet',
        description: 'The sign-in sheet shows three people visited the kitchen today: Tommy at 2pm, Sarah at 2:30pm, and Mr. Chen at 3pm.',
        location: 'Kitchen Door',
        type: 'physical',
        discovered: true,
        examined: false,
        relevance: 'important',
        imageUrl: '/clue.png'
    },

    // Case 002: The Lost School Trophy
    {
        id: 'clue-002-1',
        caseId: 'case-002',
        title: 'Dust Mark on Shelf',
        description: 'There is a clean circle on the dusty shelf where the trophy used to sit. The dust shows it was moved recently.',
        location: 'Classroom Shelf',
        type: 'physical',
        discovered: true,
        examined: false,
        relevance: 'critical',
        imageUrl: '/clue.png'
    },
    {
        id: 'clue-002-2',
        caseId: 'case-002',
        title: 'Gold Glitter',
        description: 'Tiny pieces of gold glitter are on the floor near the door. The trophy has gold glitter on it that sometimes falls off.',
        location: 'Classroom Floor',
        type: 'physical',
        discovered: true,
        examined: false,
        relevance: 'important',
        imageUrl: '/clue.png'
    },
    {
        id: 'clue-002-3',
        caseId: 'case-002',
        title: 'Student Journal',
        description: 'A journal entry from yesterday says: "I wish our class could keep the trophy in a safer place. What if someone takes it?"',
        location: 'Student Desk',
        type: 'physical',
        discovered: true,
        examined: false,
        relevance: 'important',
        imageUrl: '/clue.png'
    },

    // Case 003: The Playground Prank
    {
        id: 'clue-003-1',
        caseId: 'case-003',
        title: 'Yellow Paint',
        description: 'Small drops of yellow paint are on the ground near the swings. The paint is the same color as the smiley faces.',
        location: 'Under the Swings',
        type: 'physical',
        discovered: true,
        examined: false,
        relevance: 'critical',
        imageUrl: '/clue.png'
    },
    {
        id: 'clue-003-2',
        caseId: 'case-003',
        title: 'Art Room Key',
        description: 'Someone borrowed the art room key yesterday after school. The sign-out book shows who took it.',
        location: 'Office Desk',
        type: 'physical',
        discovered: true,
        examined: false,
        relevance: 'critical',
        imageUrl: '/clue.png'
    },
    {
        id: 'clue-003-3',
        caseId: 'case-003',
        title: 'Paintbrush',
        description: 'A small paintbrush was found in the bushes near the playground. It still has yellow paint on it.',
        location: 'Playground Bushes',
        type: 'physical',
        discovered: true,
        examined: false,
        relevance: 'important',
        imageUrl: '/clue.png'
    }
];

export const defaultSuspects: Suspect[] = [
    // Case 001: The Missing Cookie Recipe
    {
        id: 'suspect-001-1',
        caseId: 'case-001',
        name: 'Tommy Rodriguez',
        description: 'A 7-year-old student who loves cookies. He is in second grade.',
        background: 'Tommy really loves chocolate chip cookies. He asked Mrs. Baker many times for the recipe. Tommy was in the kitchen at 2pm today.',
        motive: 'Tommy wanted to make the cookies at home with his mom. He thought if he had the recipe, they could make them together.',
        alibi: 'Tommy says he only looked at the recipe card but put it back. He then went to play outside.',
        isGuilty: false,
        interviewed: false,
        imageUrl: '/suspect.png'
    },
    {
        id: 'suspect-001-2',
        caseId: 'case-001',
        name: 'Sarah Chen',
        description: 'A 8-year-old student who is really good at baking. She is in third grade.',
        background: 'Sarah loves to bake and wants to win the bake sale contest. She came to the kitchen at 2:30pm. She had chocolate on her hands from eating a brownie.',
        motive: 'Sarah wanted to use the recipe to make cookies better than anyone else at the bake sale.',
        alibi: 'Sarah says she was just looking around the kitchen. She says she didn\'t touch the recipe card.',
        isGuilty: true,
        interviewed: false,
        imageUrl: '/suspect.png'
    },
    {
        id: 'suspect-001-3',
        caseId: 'case-001',
        name: 'Mr. Chen',
        description: 'The school janitor who keeps everything clean and organized.',
        background: 'Mr. Chen cleans the kitchen every day at 3pm. He is very careful with papers and always asks before moving things.',
        motive: 'Mr. Chen might have moved the recipe while cleaning up. He likes to keep the kitchen very neat.',
        alibi: 'Mr. Chen says he saw the recipe on the desk but didn\'t touch it. He was cleaning the other side of the room.',
        isGuilty: false,
        interviewed: false,
        imageUrl: '/suspect.png'
    },

    // Case 002: The Lost School Trophy
    {
        id: 'suspect-002-1',
        caseId: 'case-002',
        name: 'Emma Wilson',
        description: 'A student who really cares about the class. She is 8 years old.',
        background: 'Emma was worried someone might steal the trophy. She wrote in her journal about keeping it safe. She stayed after school yesterday.',
        motive: 'Emma wanted to hide the trophy in a safer place. She was worried it might get lost or broken.',
        alibi: 'Emma says she was in the library after school. But the librarian saw her leave early.',
        isGuilty: true,
        interviewed: false,
        imageUrl: '/suspect.png'
    },
    {
        id: 'suspect-002-2',
        caseId: 'case-002',
        name: 'Jake Martinez',
        description: 'A student who loves science. He helped win the trophy.',
        background: 'Jake worked really hard on the science project. He is very proud of winning the trophy. He wanted to show it to his family.',
        motive: 'Jake wanted to take the trophy home for one night to show his grandparents who were visiting.',
        alibi: 'Jake says he was at soccer practice after school. His coach says he was there the whole time.',
        isGuilty: false,
        interviewed: false,
        imageUrl: '/suspect.png'
    },
    {
        id: 'suspect-002-3',
        caseId: 'case-002',
        name: 'Mrs. Patterson',
        description: 'The classroom teacher who is proud of her students.',
        background: 'Mrs. Patterson was very happy when the class won the trophy. She sometimes moves things to keep the classroom organized.',
        motive: 'Mrs. Patterson might have moved the trophy to a display case to keep it safe and show it off better.',
        alibi: 'Mrs. Patterson says she had a meeting yesterday after school. Other teachers saw her there.',
        isGuilty: false,
        interviewed: false,
        imageUrl: '/suspect.png'
    },

    // Case 003: The Playground Prank
    {
        id: 'suspect-003-1',
        caseId: 'case-003',
        name: 'Lily Anderson',
        description: 'A creative 7-year-old who loves art class.',
        background: 'Lily is the best artist in her class. She always draws smiley faces on her papers. She borrowed the art room key yesterday to work on a special project.',
        motive: 'Lily wanted to make the playground more cheerful and fun. She thought smiley faces would make kids happy.',
        alibi: 'Lily says she was working on a painting in the art room. She says she didn\'t go to the playground.',
        isGuilty: true,
        interviewed: false,
        imageUrl: '/suspect.png'
    },
    {
        id: 'suspect-003-2',
        caseId: 'case-003',
        name: 'Max Cooper',
        description: 'An 8-year-old who likes to play jokes and make people laugh.',
        background: 'Max loves funny pranks that don\'t hurt anyone. He was at school late yesterday helping his teacher. He likes to draw smiley faces too.',
        motive: 'Max thought painting smiley faces would be a funny joke that would make everyone smile.',
        alibi: 'Max says he was helping his teacher carry books to her car. His teacher says this is true.',
        isGuilty: false,
        interviewed: false,
        imageUrl: '/suspect.png'
    },
    {
        id: 'suspect-003-3',
        caseId: 'case-003',
        name: 'Coach Davis',
        description: 'The PE teacher who teaches kids sports and games.',
        background: 'Coach Davis uses the playground every day. He likes to keep things fun and colorful. He has paint in his office for marking the sports field.',
        motive: 'Coach Davis might have wanted to make the playground more fun and colorful for the kids.',
        alibi: 'Coach Davis says he left school early yesterday for a doctor appointment. The office has a record of his early departure.',
        isGuilty: false,
        interviewed: false,
        imageUrl: '/suspect.png'
    }
];
