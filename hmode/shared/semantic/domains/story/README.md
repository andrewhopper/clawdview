# Story Domain Model

Canonical story generation domain model based on W3C RDF/OWL standards. Validated against 10 classic children's books.

## 1.0 Overview

**Domain:** Narrative story generation and representation

**Version:** 1.0.0

**Standards:** W3C RDF, OWL, SHACL

**Languages:** TypeScript, Rust, Python

**Validated Against:** 10 classic children's books (Make Way for Ducklings, Where the Wild Things Are, Charlotte's Web, The Very Hungry Caterpillar, Goodnight Moon, Harold and the Purple Crayon, The Giving Tree, Green Eggs and Ham, Corduroy, The Snowy Day)

## 2.0 Key Features

This domain model addresses critical gaps found in traditional story models by supporting:

### 2.1 TIME MODELING (High Priority)

**Model character aging across life stages - boy as child vs elderly**

**Entities:**
- `TimePoint` - Moment in timeline ("childhood", "Monday", "age 8", "elderly")
- `CharacterAtTime` - Character appearance at specific time
- `StoryTimeline` - Overall story timeline with duration
- `TimeOfDay` - Specific time (7:00 PM → 8:10 PM)
- `Season` / `SeasonalProgression` - Seasonal changes

**Example:** The Giving Tree
```typescript
const boy: Character = {
  id: 'char-boy',
  name: 'The Boy',
  characterType: CharacterType.Human,
  role: CharacterRole.Protagonist,
  appearanceAtTime: [
    {
      id: 'boy-child',
      characterId: 'char-boy',
      timePointId: 'time-childhood',
      age: { type: 'stage', stage: LifeStage.Child },
      physicalDescription: 'Young, energetic, full of hair',
      emotionalState: 'Carefree, joyful',
      appearance: {
        hairAmount: 'full',
        posture: 'upright',
        expression: 'happy'
      },
    },
    {
      id: 'boy-elderly',
      characterId: 'char-boy',
      timePointId: 'time-elderly',
      age: { type: 'stage', stage: LifeStage.Elderly },
      physicalDescription: 'Stooped, wrinkled, no hair',
      emotionalState: 'Tired, weary',
      appearance: {
        hairAmount: 'none',
        posture: 'stooped',
        expression: 'sour'
      },
    },
  ],
};
```

### 2.2 TRANSFORMATION (High Priority)

**Model physical transformations - caterpillar → butterfly**

**Entities:**
- `Transformation` - State change with type, duration, trigger
- `TransformationType` - Metamorphosis, Aging, Magical, Imaginary, Environmental

**Example:** The Very Hungry Caterpillar
```typescript
const metamorphosis: Transformation = {
  id: 'transform-001',
  subjectId: 'char-caterpillar',
  fromState: {
    form: 'caterpillar',
    description: 'Small, very hungry caterpillar',
  },
  toState: {
    form: 'butterfly',
    description: 'Large, beautiful butterfly with colorful wings',
  },
  transformationType: TransformationType.Metamorphosis,
  duration: '2 weeks',
  trigger: 'Spending time in cocoon',
};
```

### 2.3 REALITY STATUS (High Priority)

**Distinguish real vs imaginary elements**

**Entities:**
- `RealityStatus` - Real, imaginary, perspective-dependent

**Example:** Harold and the Purple Crayon
```typescript
const moon: Object = {
  id: 'obj-moon',
  name: 'Moon',
  type: ObjectType.NaturalObject,
  description: 'Moon drawn by Harold to light his walk',
  isSymbolic: false,
  realityStatus: {
    isReal: false,
    isImaginary: true,
    imaginedBy: 'char-harold',
  },
  createdBy: 'char-harold',
  creationMethod: 'Drawn with purple crayon',
};

const bedroom: Location = {
  id: 'loc-bedroom',
  name: "Max's Bedroom",
  type: LocationType.Indoor,
  isRealWorld: true,
  realityStatus: {
    isReal: true,
    isImaginary: false,
  },
};

const wildThingsLand: Location = {
  id: 'loc-wild-things',
  name: 'Land of the Wild Things',
  type: LocationType.Natural,
  isRealWorld: false,
  realityStatus: {
    isReal: false,
    isImaginary: true,
    imaginedBy: 'char-max',
    perspective: "From Max's imagination during timeout",
  },
};
```

### 2.4 REPETITIVE PATTERNS (Medium Priority)

**Model repeated scenes with variations**

**Entities:**
- `RepetitivePattern` - Pattern type, base content, variations
- `Variation` - Individual occurrence with location/order

**Example:** Green Eggs and Ham
```typescript
const greenEggsPattern: RepetitivePattern = {
  id: 'pattern-001',
  storyId: 'story-green-eggs',
  patternType: PatternType.QuestionAnswer,
  baseContent: 'Would you eat them',
  occurrences: 8,
  variations: [
    { content: 'Would you eat them in a house?', order: 1 },
    { content: 'Would you eat them in a box?', order: 2 },
    { content: 'Would you eat them in a car?', order: 3 },
    { content: 'Would you eat them in a tree?', order: 4 },
    { content: 'Would you eat them in a train?', order: 5 },
    { content: 'Would you eat them in the dark?', order: 6 },
    { content: 'Would you eat them in the rain?', order: 7 },
    { content: 'Would you eat them in a boat?', order: 8 },
  ],
};
```

**Example:** Goodnight Moon
```typescript
const goodnightRitual: RepetitivePattern = {
  id: 'pattern-goodnight',
  storyId: 'story-goodnight-moon',
  patternType: PatternType.Ritual,
  baseContent: 'Goodnight',
  occurrences: 20,
  variations: [
    { content: 'Goodnight room', order: 1 },
    { content: 'Goodnight moon', order: 2 },
    { content: 'Goodnight cow jumping over the moon', order: 3 },
    { content: 'Goodnight light', order: 4 },
    { content: 'Goodnight red balloon', order: 5 },
    // ... 15 more
    { content: 'Goodnight noises everywhere', order: 20 },
  ],
};
```

### 2.5 OBJECT INVENTORIES (Medium Priority)

**Catalog every object in a location**

**Entities:**
- `ObjectInventory` - Complete catalog for location
- `CatalogedObject` - Object with position and significance

**Example:** Goodnight Moon
```typescript
const greatGreenRoom: Location = {
  id: 'loc-green-room',
  name: 'Great Green Room',
  type: LocationType.Indoor,
  description: 'Cozy bedroom with fireplace',
  isRealWorld: false,
  inventory: {
    locationId: 'loc-green-room',
    purpose: InventoryPurpose.BedrimeRitual,
    objects: [
      {
        objectId: 'obj-telephone',
        position: 'on table',
        addressedDirectly: true,
      },
      {
        objectId: 'obj-balloon',
        position: 'floating near ceiling',
        addressedDirectly: true,
      },
      {
        objectId: 'obj-cow-picture',
        position: 'on wall',
        significance: 'Bedtime ritual object',
        addressedDirectly: true,
      },
      {
        objectId: 'obj-socks',
        position: 'drying near fireplace',
        addressedDirectly: true,
      },
      {
        objectId: 'obj-mittens',
        position: 'near fireplace',
        addressedDirectly: true,
      },
      {
        objectId: 'obj-kittens',
        position: 'playing on carpet',
        addressedDirectly: true,
      },
      {
        objectId: 'obj-mouse',
        position: 'peeking out from corner',
        addressedDirectly: true,
      },
      {
        objectId: 'obj-mush',
        position: 'in bowl on table',
        addressedDirectly: true,
      },
    ],
  },
};
```

### 2.6 SYMBOLIC OBJECTS (Medium Priority)

**Objects with deeper meaning**

**Entities:**
- `Symbol` - Concept, interpretation, cultural context
- `isSymbolic` flag on Object

**Example:** Corduroy's Button
```typescript
const button: Object = {
  id: 'obj-button',
  name: 'Missing Button',
  type: ObjectType.Prop,
  description: 'Button missing from Corduroy\'s overalls',
  isSymbolic: true,
  symbolism: 'Not belonging, being incomplete or imperfect',
  symbolizes: [
    {
      concept: 'Belonging',
      interpretation: 'Missing button represents not belonging; sewn button represents acceptance',
      culturalContext: 'Universal theme of acceptance despite imperfections',
    },
    {
      concept: 'Love and Acceptance',
      interpretation: 'Lisa sews button showing unconditional love',
    },
  ],
};
```

**Example:** The Snowy Day Snowball
```typescript
const snowball: Object = {
  id: 'obj-snowball',
  name: 'Snowball in Pocket',
  type: ObjectType.NaturalObject,
  description: 'Snowball Peter puts in pocket to save',
  isSymbolic: true,
  symbolism: 'Inability to preserve childhood moments',
  symbolizes: [
    {
      concept: 'Impermanence',
      interpretation: 'Snowball melts, teaching that some moments cannot be preserved',
    },
  ],
};
```

### 2.7 ANTHROPOMORPHIC TRAITS (Medium Priority)

**Distinguish realistic animals from talking animals**

**Entities:**
- `CharacterType` enum - Human, Animal, AnthropomorphicAnimal, etc.
- `AnthropomorphicTrait` enum - Speech, Clothing, HumanEmotions, etc.

**Example:** Make Way for Ducklings (Realistic)
```typescript
const mrsMallard: Character = {
  id: 'char-mrs-mallard',
  name: 'Mrs. Mallard',
  characterType: CharacterType.Animal,
  species: 'Mallard duck',
  role: CharacterRole.Protagonist,
  description: 'Mother duck looking for safe place to raise ducklings',
  anthropomorphicTraits: [], // Realistic animal, no human traits
};
```

**Example:** Charlotte's Web (Anthropomorphic)
```typescript
const charlotte: Character = {
  id: 'char-charlotte',
  name: 'Charlotte A. Cavatica',
  characterType: CharacterType.AnthropomorphicAnimal,
  species: 'Barn spider',
  role: CharacterRole.Supporting,
  description: 'Wise spider who befriends Wilbur',
  anthropomorphicTraits: [
    AnthropomorphicTrait.Speech,
    AnthropomorphicTrait.HumanEmotions,
    AnthropomorphicTrait.UsesTools, // Uses web as writing tool
  ],
};
```

**Example:** Goodnight Moon (Anthropomorphic)
```typescript
const bunny: Character = {
  id: 'char-bunny',
  name: 'Little Bunny',
  characterType: CharacterType.AnthropomorphicAnimal,
  species: 'Rabbit',
  role: CharacterRole.Protagonist,
  anthropomorphicTraits: [
    AnthropomorphicTrait.Speech,
    AnthropomorphicTrait.Clothing, // Wears pajamas
    AnthropomorphicTrait.HumanEmotions,
  ],
};
```

### 2.8 CHARACTER GROUPS (Medium Priority)

**Groups with individual traits per member**

**Entities:**
- `CharacterGroup` - Group name, type, members
- `GroupMember` - Distinctive traits for each member

**Example:** Make Way for Ducklings (8 Ducklings)
```typescript
const ducklings: CharacterGroup = {
  id: 'group-ducklings',
  name: 'The Ducklings',
  groupType: GroupType.Siblings,
  members: [
    {
      characterId: 'char-jack',
      distinctiveTraits: ['Inquisitive', 'Looks around curiously'],
      role: 'Eldest',
    },
    {
      characterId: 'char-kack',
      distinctiveTraits: ['Sleepy', 'Often lags behind'],
    },
    {
      characterId: 'char-lack',
      distinctiveTraits: ['Talkative', 'Quacks frequently'],
    },
    {
      characterId: 'char-mack',
      distinctiveTraits: ['Energetic', 'Runs to catch up'],
    },
    {
      characterId: 'char-nack',
      distinctiveTraits: ['Cautious', 'Stays close to mother'],
    },
    {
      characterId: 'char-ouack',
      distinctiveTraits: ['Bored', 'Looks distracted'],
    },
    {
      characterId: 'char-pack',
      distinctiveTraits: ['Scratching', 'Often preening'],
    },
    {
      characterId: 'char-quack',
      distinctiveTraits: ['Playful', 'Youngest of siblings'],
      role: 'Youngest',
    },
  ],
};
```

## 3.0 Complete Example: The Giving Tree

Demonstrating time modeling, transformation, and character aging:

```typescript
// Timeline
const timeline: StoryTimeline = {
  storyId: 'story-giving-tree',
  duration: 'a lifetime',
  timePoints: [
    {
      id: 'time-childhood',
      timestamp: 'childhood',
      description: 'Boy plays with tree as child',
    },
    {
      id: 'time-teenager',
      timestamp: 'teenage years',
      description: 'Boy returns as teenager wanting money',
    },
    {
      id: 'time-young-adult',
      timestamp: 'young adulthood',
      description: 'Boy returns wanting house',
    },
    {
      id: 'time-middle-age',
      timestamp: 'middle age',
      description: 'Boy returns wanting boat',
    },
    {
      id: 'time-elderly',
      timestamp: 'old age',
      description: 'Boy returns as elderly man wanting rest',
    },
  ],
};

// Boy aging transformation
const boyAging: Transformation = {
  id: 'transform-boy-aging',
  subjectId: 'char-boy',
  fromState: {
    stage: LifeStage.Child,
    description: 'Young, carefree, full of energy',
  },
  toState: {
    stage: LifeStage.Elderly,
    description: 'Old, tired, stooped and wrinkled',
  },
  transformationType: TransformationType.Aging,
  duration: 'a lifetime',
  trigger: 'Passage of time',
};

// Tree transformation
const treeTransformation: Transformation = {
  id: 'transform-tree',
  subjectId: 'char-tree',
  fromState: {
    form: 'Full tree',
    description: 'Tall tree with branches, leaves, apples',
  },
  toState: {
    form: 'Stump',
    description: 'Just a stump remaining',
  },
  transformationType: TransformationType.Environmental,
  duration: 'a lifetime',
  trigger: 'Giving everything to the boy',
};

// Story
const givingTree: Story = {
  id: 'story-giving-tree',
  title: 'The Giving Tree',
  author: 'Shel Silverstein',
  publicationYear: 1964,
  status: StoryStatus.Published,
  genre: GenreType.Literary,
  timeline,
  characters: [boy, tree],
  scenes: [...], // Multiple scenes across different time points
  themes: [
    { concept: 'Unconditional love' },
    { concept: 'Giving vs taking' },
    { concept: 'Aging and mortality' },
    { concept: 'Sacrifice' },
  ],
};
```

## 4.0 Use Cases

### 4.1 Story Generation Application

```typescript
import { Story, Character, Scene, validateStory } from '@shared/domain-models/story/generated/typescript';

// Generate story with character aging
const story = generateStoryWithAging({
  protagonist: {
    name: 'Sarah',
    ageProgression: [
      { stage: LifeStage.Child, description: 'Curious 8-year-old' },
      { stage: LifeStage.Teenager, description: 'Rebellious 16-year-old' },
      { stage: LifeStage.YoungAdult, description: 'Confident 25-year-old' },
    ],
  },
  theme: 'Coming of age',
});

const validation = validateStory(story);
if (!validation.valid) {
  console.error('Story validation failed:', validation.errors);
}
```

### 4.2 Children's Book Generator

```typescript
// Generate book with repetitive pattern (like Green Eggs and Ham)
const book = generateRepetitiveBook({
  baseQuestion: 'Would you like to try',
  variations: ['in a park', 'on a boat', 'with a goat', 'in the rain'],
  protagonist: { name: 'Sam', type: CharacterType.Human },
  theme: 'Trying new things',
});
```

### 4.3 Interactive Story Editor

```typescript
// Track character across multiple scenes at different ages
const character: Character = {
  id: 'char-001',
  name: 'Emma',
  characterType: CharacterType.Human,
  role: CharacterRole.Protagonist,
  appearanceAtTime: [
    createCharacterAtTime(character, 'scene-1', LifeStage.Child),
    createCharacterAtTime(character, 'scene-10', LifeStage.Teenager),
    createCharacterAtTime(character, 'scene-20', LifeStage.MiddleAged),
  ],
};
```

## 5.0 Validation Rules

All SHACL constraints enforced:

**Story:**
- Title required (1-200 characters)
- Status required
- At least one character required
- At least one scene required
- Published stories must be Complete first

**Character:**
- Name required (1-100 characters)
- Character type required
- Role required
- Anthropomorphic animals should have species defined

**Scene:**
- Scene number required (positive integer)
- Location required
- Content required (not empty)

**Location:**
- Name required (1-200 characters)
- Type required
- Real-world locations should have city/state

**Object:**
- Name required (1-200 characters)
- Type required
- Symbolic objects should have symbolism defined

**TimePoint:**
- Timestamp required

**CharacterAtTime:**
- Time point reference required
- Physical description required

**Transformation:**
- Type required
- From state required
- To state required

**RepetitivePattern:**
- Pattern type required
- Base content required
- Occurrences must be 2+

**CharacterGroup:**
- Name required
- Must have 2+ members

## 6.0 Files

```
story/
├── ontology.ttl              # W3C RDF/OWL canonical model (771 lines)
├── rules.shacl.ttl           # SHACL validation constraints (427 lines)
├── version.json              # Semantic version metadata
├── README.md                 # This file
├── ANALYSIS.md               # 10-book analysis with gap identification
└── generated/
    └── typescript/
        └── story.types.ts    # TypeScript types (1,156 lines)
```

## 7.0 Books Analyzed

1. **Make Way for Ducklings** (1941) - Robert McCloskey
   - Realistic animals, real-world Boston locations, character groups

2. **Where the Wild Things Are** (1963) - Maurice Sendak
   - Real vs imaginary locations, environmental transformation

3. **Charlotte's Web** (1952) - E.B. White
   - Anthropomorphic animals, seasonal progression, aging, themes

4. **The Very Hungry Caterpillar** (1969) - Eric Carle
   - Metamorphosis transformation, time progression

5. **Goodnight Moon** (1947) - Margaret Wise Brown
   - Object inventory, repetitive ritual, time of day progression

6. **Harold and the Purple Crayon** (1955) - Crockett Johnson
   - Imaginary object creation, reality status

7. **The Giving Tree** (1964) - Shel Silverstein
   - Character aging across lifetime, transformation

8. **Green Eggs and Ham** (1960) - Dr. Seuss
   - Repetitive question-answer pattern, linguistic constraints

9. **Corduroy** (1968) - Don Freeman
   - Symbolic objects, real-world locations (department store)

10. **The Snowy Day** (1962) - Ezra Jack Keats
    - Real-world city location, symbolic objects

## 8.0 Standards Used

**W3C:**
- RDF: https://www.w3.org/RDF/
- OWL: https://www.w3.org/OWL/
- SHACL: https://www.w3.org/TR/shacl/
- Schema.org: https://schema.org/

## 9.0 Version History

**1.0.0** (2025-11-21)
- Initial release
- High priority: Time modeling, transformation, reality status, character at time
- Medium priority: Repetitive patterns, object inventories, symbolic objects, anthropomorphic traits, character groups
- Validated against 10 classic children's books
- TypeScript, Rust, Python type generation

## 10.0 Future Enhancements

**Planned:**
- Visual style progression (illustrations grow/darken)
- Linguistic constraints (word count, vocabulary limits)
- Plot templates (hero's journey, three-act structure)
- Emotional arcs (character emotional development)
- Narrative voice (first person, third person omniscient)

## 11.0 Related Documentation

- **Analysis:** See `ANALYSIS.md` for complete gap analysis
- **Domain Models:** See `../README.md` for domain model architecture
- **Generator:** See `../../tools/domain-generator/README.md` for type generation

---

**Questions? Run:** `/generate-domain story --help`
