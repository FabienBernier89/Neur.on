# Traduction automatique par Corrext (LexMachina)

Relevé le 2026-10-02 sur la page « Fast translation » de corrext.com, dans la session de Fabien (accord du 2026-10-02 pour traduire le site).

## Appel

`POST https://api.corrext.com/api/v1/translation/translate`

En-têtes : `Authorization: Bearer <jeton de session>`, `Content-Type: application/json`, `Accept: application/json`. Le jeton vient de `https://corrext.com/api/auth/session` (champ `accessToken`). Il n'est jamais affiché, copié ni écrit : il reste dans l'onglet du navigateur.

Corps :

```json
{"texts": ["…", "…"], "sourceLanguageId": 51, "targetLanguageId": 46, "providerId": 1, "projectId": null}
```

Réponse :

```json
{"texts": [{"text": "…", "matchRate": 30.0}], "sourceLanguageId": 51}
```

- `texts` est une liste : plusieurs segments par appel.
- `sourceLanguageId: null` déclenche la détection de la langue.
- Limite de l'interface : 10 000 caractères par texte.

| Langue | Identifiant |
|---|---|
| français | 51 |
| allemand | 46 |
| italien | 140 |
| anglais | 56 |

| Moteur | `providerId` |
|---|---|
| LexMachina | 1 |

## Balisage en ligne

Test sur 5 formes de marqueurs (FR vers DE) :

| Forme | Résultat |
|---|---|
| `<a id="1">…</a>`, `<x1>…</x1>` | balise vidée, texte sorti de la balise : inutilisable |
| `[[1]]…[[/1]]` | parfois abîmé (`[[1]`) |
| `§1§…§/1§` | abîmé (`§/1 §`) |
| `⟦1⟧…⟦/1⟧` | espaces ajoutées, accord parfois faux |
| `{1}…{/1}` | intact, espaces ajoutées à l'intérieur : **retenu** |
| `XA1 … XZ1` | intact |

Forme retenue : `{n}…{/n}`, et `{n}` seul pour un élément sans contenu (`<br>`, jeton `{{…}}`). À la lecture, les espaces ajoutées autour des marqueurs sont retirées. Un segment dont les marqueurs reviennent manquants ou en double repart sans balisage : l'agent d'adaptation remet les liens d'après le FR.

Remarque : en italien, LexMachina emploie de lui-même le vouvoiement au pluriel (« Consultate »), conforme au guide.
