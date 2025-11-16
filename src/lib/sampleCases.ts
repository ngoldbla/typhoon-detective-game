import { v4 as uuidv4 } from 'uuid';
import { Case, Clue, Suspect } from '@/types/game';

// Generate IDs for cases
const missingPetId = uuidv4();
const libraryBookId = uuidv4();
const lunchBoxId = uuidv4();

// Sample Cases
export const sampleCases: Case[] = [
    {
        id: missingPetId,
        title: "The Missing Class Pet",
        description: "Fluffy the class hamster is missing from her cage! The cage door is open but nobody knows how. Fluffy loves to hide in small spaces. We need to find her before she gets scared or hungry.",
        summary: "Help find Fluffy the hamster who escaped from her cage in the classroom.",
        difficulty: 'easy',
        solved: false,
        location: "Second Grade Classroom",
        dateTime: "2024-05-15T09:30:00Z",
        imageUrl: "https://images.unsplash.com/photo-1425082661705-1834bfd09dca",
        isLLMGenerated: false
    },
    {
        id: libraryBookId,
        title: "The Library Book Mystery",
        description: "The special book about dinosaurs is missing from the library! It was the last copy and lots of kids wanted to read it. Someone checked it out last week but forgot to write their name. The librarian needs help finding who has the book.",
        summary: "Find out who has the missing dinosaur book from the school library.",
        difficulty: 'medium',
        solved: false,
        location: "School Library",
        dateTime: "2024-06-02T13:15:00Z",
        imageUrl: "https://images.unsplash.com/photo-1481627834876-b7833e8f5570",
        isLLMGenerated: false
    },
    {
        id: lunchBoxId,
        title: "The Switched Lunch Box",
        description: "Someone took the wrong lunch box today! Maya brought her favorite lunch with a peanut butter sandwich. Now she has someone else's lunch box with a turkey sandwich. Both lunch boxes are blue. We need to find out whose lunch box Maya has so everyone gets the right lunch.",
        summary: "Help Maya find her real lunch box and return the one she has by mistake.",
        difficulty: 'easy',
        solved: false,
        location: "School Cafeteria",
        dateTime: "2024-04-10T12:00:00Z",
        imageUrl: "https://images.unsplash.com/photo-1546069901-ba9599a7e63c",
        isLLMGenerated: false
    }
];

// Clues for The Missing Class Pet
export const missingPetClues: Clue[] = [
    {
        id: uuidv4(),
        caseId: missingPetId,
        title: "Cage door open",
        description: "The cage door is open. The latch is easy to open from outside. A child could open it, but Fluffy cannot open it from inside.",
        location: "Hamster cage on the shelf",
        type: "physical",
        discovered: true,
        examined: false,
        relevance: "critical"
    },
    {
        id: uuidv4(),
        caseId: missingPetId,
        title: "Tiny footprints",
        description: "There are tiny hamster footprints on the desk near the cage. The footprints lead toward the reading corner.",
        location: "Teacher's desk",
        type: "physical",
        discovered: true,
        examined: false,
        relevance: "important"
    },
    {
        id: uuidv4(),
        caseId: missingPetId,
        title: "Note from a student",
        description: "A note found on the floor says 'I want to pet Fluffy. She is so soft and cute.'",
        location: "Floor near the cage",
        type: "physical",
        discovered: true,
        examined: false,
        relevance: "important"
    },
    {
        id: uuidv4(),
        caseId: missingPetId,
        title: "Missing sunflower seed",
        description: "One sunflower seed from Fluffy's food dish is missing. Someone might have used it to get Fluffy to come out.",
        location: "Food dish in cage",
        type: "physical",
        discovered: true,
        examined: false,
        relevance: "minor"
    }
];

// Suspects for The Missing Class Pet
export const missingPetSuspects: Suspect[] = [
    {
        id: uuidv4(),
        caseId: missingPetId,
        name: "Oliver Chen",
        description: "A 7-year-old who really loves animals",
        background: "Oliver asks to hold Fluffy every day. He is very gentle with animals. He was the first one to notice Fluffy was missing this morning.",
        motive: "Oliver wanted to play with Fluffy. He might have opened the cage to pet her and forgot to close it.",
        alibi: "Oliver says he just looked at Fluffy through the cage. He didn't touch the cage door.",
        interviewed: false,
        isGuilty: true
    },
    {
        id: uuidv4(),
        caseId: missingPetId,
        name: "Zoe Martinez",
        description: "A student who helps the teacher take care of Fluffy",
        background: "Zoe feeds Fluffy every morning before class starts. She is very responsible and always closes the cage carefully.",
        motive: "Zoe feeds Fluffy every day. She might have forgotten to close the cage after feeding her this morning.",
        alibi: "Zoe says she fed Fluffy and made sure the door was locked. She checked it twice like always.",
        interviewed: false,
        isGuilty: false
    },
    {
        id: uuidv4(),
        caseId: missingPetId,
        name: "Ryan Taylor",
        description: "A curious 8-year-old who likes to explore",
        background: "Ryan loves to watch Fluffy run on her wheel. He drew a picture of Fluffy last week. He was at school very early this morning.",
        motive: "Ryan might have wanted to see Fluffy up close. He could have opened the cage to watch her better.",
        alibi: "Ryan says he was in the library reading books this morning before class started.",
        interviewed: false,
        isGuilty: false
    }
];

// Clues for The Library Book Mystery
export const libraryBookClues: Clue[] = [
    {
        id: uuidv4(),
        caseId: libraryBookId,
        title: "Checkout card",
        description: "The book checkout card has a name on it, but someone erased it. You can still see the shape of the letters through the eraser marks.",
        location: "Library checkout desk",
        type: "physical",
        discovered: true,
        examined: false,
        relevance: "critical"
    },
    {
        id: uuidv4(),
        caseId: libraryBookId,
        title: "Dinosaur drawing",
        description: "A drawing of a T-Rex was found in the art room. It looks like someone traced it from a book. The drawing is very detailed.",
        location: "Art room table",
        type: "physical",
        discovered: true,
        examined: false,
        relevance: "important"
    },
    {
        id: uuidv4(),
        caseId: libraryBookId,
        title: "Book report topic list",
        description: "The teacher has a list of book report topics. Three students picked dinosaurs: Alex, Jordan, and Riley.",
        location: "Teacher's desk",
        type: "physical",
        discovered: true,
        examined: false,
        relevance: "important"
    },
    {
        id: uuidv4(),
        caseId: libraryBookId,
        title: "Torn bookmark",
        description: "A bookmark with dinosaurs on it was found torn in half near the library return slot. The top half is missing.",
        location: "Book return box",
        type: "physical",
        discovered: true,
        examined: false,
        relevance: "minor"
    }
];

// Suspects for The Library Book Mystery
export const libraryBookSuspects: Suspect[] = [
    {
        id: uuidv4(),
        caseId: libraryBookId,
        name: "Alex Johnson",
        description: "A student who loves dinosaurs and knows everything about them",
        background: "Alex has dinosaur posters in their room at home. Alex is doing a book report on T-Rex. Alex has been looking for good dinosaur books.",
        motive: "Alex wanted to keep the book longer to finish the book report. They were worried someone else would check it out.",
        alibi: "Alex says they returned the book on time. But the librarian didn't see them return it.",
        interviewed: false,
        isGuilty: false
    },
    {
        id: uuidv4(),
        caseId: libraryBookId,
        name: "Jordan Lee",
        description: "A forgetful student who sometimes loses things",
        background: "Jordan often forgets to return library books on time. Jordan's mom had to pay late fees last month. Jordan is working on a dinosaur project.",
        motive: "Jordan probably forgot the book was due. Jordan might still have it in their backpack at home.",
        alibi: "Jordan says they thought the book was already returned. Jordan isn't sure when they last saw it.",
        interviewed: false,
        isGuilty: true
    },
    {
        id: uuidv4(),
        caseId: libraryBookId,
        name: "Riley Parker",
        description: "A student who is very careful with books",
        background: "Riley loves to read and always returns books on time. Riley is also writing about dinosaurs. Riley has a bookmark with dinosaurs on it.",
        motive: "Riley might have wanted to use the book for longer. Riley could have erased their name to check it out again.",
        alibi: "Riley says they saw the book in the library last week but didn't check it out. Riley is using other books instead.",
        interviewed: false,
        isGuilty: false
    }
];

// Clues for The Switched Lunch Box
export const lunchBoxClues: Clue[] = [
    {
        id: uuidv4(),
        caseId: lunchBoxId,
        title: "Name tag",
        description: "The lunch box Maya has now has a name tag that fell off. The tag is on the cafeteria floor. It says 'Ben'.",
        location: "Cafeteria floor",
        type: "physical",
        discovered: true,
        examined: false,
        relevance: "critical"
    },
    {
        id: uuidv4(),
        caseId: lunchBoxId,
        title: "Turkey sandwich note",
        description: "There is a note in the lunch box Maya has. It says 'Enjoy your sandwich! Love, Dad' in messy handwriting.",
        location: "Inside the lunch box",
        type: "physical",
        discovered: true,
        examined: false,
        relevance: "important"
    },
    {
        id: uuidv4(),
        caseId: lunchBoxId,
        title: "Blue lunch boxes list",
        description: "The cafeteria helper made a list of students with blue lunch boxes. Four students have blue lunch boxes today.",
        location: "Cafeteria desk",
        type: "physical",
        discovered: true,
        examined: false,
        relevance: "important"
    }
];

// Suspects for The Switched Lunch Box
export const lunchBoxSuspects: Suspect[] = [
    {
        id: uuidv4(),
        caseId: lunchBoxId,
        name: "Ben Rodriguez",
        description: "A student who sits near Maya in the cafeteria",
        background: "Ben has a blue lunch box just like Maya's. Ben's dad makes his lunch every morning. Ben loves turkey sandwiches.",
        motive: "Ben probably grabbed the wrong blue lunch box by mistake. The lunch boxes look exactly the same.",
        alibi: "Ben says he took his own lunch box. He didn't notice it was the wrong one until he opened it.",
        interviewed: false,
        isGuilty: true
    },
    {
        id: uuidv4(),
        caseId: lunchBoxId,
        name: "Emma Wilson",
        description: "A student who was very hungry today",
        background: "Emma forgot her lunch at home this morning. She was very sad because she was hungry. Emma's mom brings her lunch sometimes.",
        motive: "Emma might have taken Maya's lunch box because she forgot hers and was really hungry.",
        alibi: "Emma says her mom brought her lunch from home. She has her own food to eat now.",
        interviewed: false,
        isGuilty: false
    },
    {
        id: uuidv4(),
        caseId: lunchBoxId,
        name: "Lucas Kim",
        description: "A helpful student who puts lunch boxes on the tables",
        background: "Lucas helps in the cafeteria by putting lunch boxes on the tables. Sometimes he mixes them up when many look the same.",
        motive: "Lucas was helping set up lunch boxes. He might have put the wrong blue lunch box at Maya's seat.",
        alibi: "Lucas says he tried to match each lunch box to the right person. But there were many blue lunch boxes today.",
        interviewed: false,
        isGuilty: false
    }
];

// Combined export of all sample data
export const sampleData = {
    cases: sampleCases,
    clues: [
        ...missingPetClues,
        ...libraryBookClues,
        ...lunchBoxClues
    ],
    suspects: [
        ...missingPetSuspects,
        ...libraryBookSuspects,
        ...lunchBoxSuspects
    ]
};
