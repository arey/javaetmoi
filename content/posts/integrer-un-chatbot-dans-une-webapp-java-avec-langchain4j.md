---
_edit_last: "1"
_monsterinsights_sitenote_active: ""
_monsterinsights_skip_tracking: ""
_oembed_8a22730ebdfb4f2fdf2f13beda5835c9: <iframe title="Démo du chatbot de Spring Petclinic LangChain4j" width="584" height="329" src="https://www.youtube.com/embed/hy2HDMjLr_8?feature=oembed" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
_oembed_3978532bf227102e3b98953369e19191: <iframe title="Démo du chatbot de Spring Petclinic LangChain4j" width="474" height="267" src="https://www.youtube.com/embed/hy2HDMjLr_8?feature=oembed" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
_oembed_d802e5e5901e439d1d3993d47a58cff7: <iframe title="Démo du chatbot de Spring Petclinic LangChain4j" width="500" height="281" src="https://www.youtube.com/embed/hy2HDMjLr_8?feature=oembed" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
_oembed_time_8a22730ebdfb4f2fdf2f13beda5835c9: "1731350760"
_oembed_time_3978532bf227102e3b98953369e19191: "1755437453"
_oembed_time_d802e5e5901e439d1d3993d47a58cff7: "1756755939"
author: admin
categories:
  - retour-d'expérience
  - spring
date: "2024-11-11T18:34:24+00:00"
footnotes: ""
guid: https://javaetmoi.com/?p=2391
parent_post_id: null
post_id: "2391"
post_views_count: "8220"
summary: |-
  Cet article explique comment intégrer un **chatbot** utilisant l’ **IA générative** dans une **application de gestion** codée en **Java**.

  Nous nous appuierons sur le framework Open Source [**LangChain4j**](https://docs.langchain4j.dev/), une adaptation Java de la célèbre librairie python LangChain, visant à simplifier l'intégration de grands modèles de langage ( **LLM**). LangChain4j permet de créer des **agents conversationnels**, des **assistants virtuels** (comme notre chatbot), ou des applications capables d'effectuer des **analyses de texte** et de répondre en fonction de données contextuelles, le tout sans devoir écrire de code complexe et avec un **haut niveau d’abstraction**. Elle facilite notamment l'utilisation des API des Large Langage Model comme [OpenAI](https://docs.langchain4j.dev/integrations/language-models/open-ai) et [Hugging Face](https://docs.langchain4j.dev/integrations/language-models/hugging-face), et propose différents connecteurs pour des bases de données vectorielles, incluant [Elasticsearch](https://docs.langchain4j.dev/integrations/embedding-stores/elasticsearch) et [Qdrant](https://docs.langchain4j.dev/integrations/embedding-stores/qdrant). Pour accélérer son intégration, LangChain4j propose des extensions pour **Quarkus** et des starters pour **Spring Boot**.

  Pour illustrer cet article, nous utiliserons l’illustre application démo **Spring Petclinic** et son récent fork dédié à LangChain4j : [**spring-petclinic-langchain4j**](https://github.com/spring-petclinic/spring-petclinic-langchain4j){{ double-space-with-newline }}Propulsé par Spring Boot, Spring Petclinic s’appuie sur **Spring Data JPA** pour l’accès aux données et **Thymeleaf** pour la couche présentation HTML / CSS / JavaScript.{{ double-space-with-newline }}En septembre 2024, Oded Shopen, contributeur en 2020 du fork [Spring Petclinic Cloud](https://github.com/spring-petclinic/spring-petclinic-cloud/), [a proposé une intégration de Spring AI dans Spring Petclinic](https://spring.io/blog/2024/09/26/ai-meets-spring-petclinic-implementing-an-ai-assistant-with-spring-ai-part-i). De son travail, est né le projet [spring-petclinic-ai](https://github.com/spring-petclinic/spring-petclinic-ai). Le repository [spring-petclinic-langchain4j](https://github.com/spring-petclinic/spring-petclinic-langchain4j) est un **portage** du framework **[Spring AI](https://spring.io/projects/spring-ai/)** vers **LangChain4j**. Y a été ajouté notamment une fonctionnalité de **streaming**.{{ double-space-with-newline }}Extraits du sample, les exemples de code s’appuient sur les versions 3.3 de Spring Boot et **0.35.0 de LangChaing4j**.
tags:
  - genai
  - langchain4j
  - openai
  - spring-boot
title: Intégrer un Chatbot dans une webapp Java avec LangChain4j
url: /2024/11/integrer-un-chatbot-dans-une-webapp-java-avec-langchain4j/

---
{{< figure src="/wp-content/uploads/2024/11/logo%5Flangchain4j.png" alt="Logo du framework LangChain4j" caption="Logo du framework LangChain4j" >}}

Cet article explique comment intégrer un **chatbot** utilisant l’ **IA générative** dans une **application de gestion** codée en **Java**.

Nous nous appuierons sur le framework Open Source [**LangChain4j**](https://docs.langchain4j.dev/), une adaptation Java de la célèbre librairie python LangChain, visant à simplifier l'intégration de grands modèles de langage ( **LLM**). LangChain4j permet de créer des **agents conversationnels**, des **assistants virtuels** (comme notre chatbot), ou des applications capables d'effectuer des **analyses de texte** et de répondre en fonction de données contextuelles, le tout sans devoir écrire de code complexe et avec un **haut niveau d’abstraction**. Elle facilite notamment l'utilisation des API des Large Langage Model comme [OpenAI](https://docs.langchain4j.dev/integrations/language-models/open-ai) et [Hugging Face](https://docs.langchain4j.dev/integrations/language-models/hugging-face), et propose différents connecteurs pour des bases de données vectorielles, incluant [Elasticsearch](https://docs.langchain4j.dev/integrations/embedding-stores/elasticsearch) et [Qdrant](https://docs.langchain4j.dev/integrations/embedding-stores/qdrant). Pour accélérer son intégration, LangChain4j propose des extensions pour **Quarkus** et des starters pour **Spring Boot**.

Pour illustrer cet article, nous utiliserons l’illustre application démo **Spring Petclinic** et son récent fork dédié à LangChain4j : [**spring-petclinic-langchain4j**](https://github.com/spring-petclinic/spring-petclinic-langchain4j)  
Propulsé par Spring Boot, Spring Petclinic s’appuie sur **Spring Data JPA** pour l’accès aux données et **Thymeleaf** pour la couche présentation HTML / CSS / JavaScript.  
En septembre 2024, Oded Shopen, contributeur en 2020 du fork [Spring Petclinic Cloud](https://github.com/spring-petclinic/spring-petclinic-cloud/), [a proposé une intégration de Spring AI dans Spring Petclinic](https://spring.io/blog/2024/09/26/ai-meets-spring-petclinic-implementing-an-ai-assistant-with-spring-ai-part-i). De son travail, est né le projet [spring-petclinic-ai](https://github.com/spring-petclinic/spring-petclinic-ai). Le repository [spring-petclinic-langchain4j](https://github.com/spring-petclinic/spring-petclinic-langchain4j) est un **portage** du framework **[Spring AI](https://spring.io/projects/spring-ai/)** vers **LangChain4j**. Y a été ajouté notamment une fonctionnalité de **streaming**.  
Extraits du sample, les exemples de code s’appuient sur les versions 3.3 de Spring Boot et **0.35.0 de LangChaing4j**.

## Démo

Avant de se plonger dans le code Java, je vous propose de voir le résultat final en visionnant ce **screencast** durant moins de **2 minutes** et dans lequel je pose **4 questions** à l’assistant :

https://youtu.be/hy2HDMjLr\_8

Impressionnant, non ? Lorsqu’on pose les mêmes questions en français, le chatbot répond en français.

## Compte développeur OpenAI

A ce jour, l’application Spring Petclinic LangChain4j supporte OpenAI et son service hébergé sur Azure : Azure OpenAI. Dans cet article, nous nous focaliserons sur l’intégration **OpenAI**. Pour faire fonctionner ce sample, moyennant quelques euros de crédits, vous aurez besoin d’un [compte développeur OpenAI](https://platform.openai.com/docs/quickstar) et d’une clé d’API personnelle exportée en tant que variable d’environnement **OPENAI\_API\_KEY**.

Si vous ne disposez pas de votre propre clé API OpenAI ou ne souhaitez pas dépenser le moindre centime, vous pouvez utiliser temporairement la clé de démonstration **demo** que OpenAI fournit gratuitement. Seul le modèle **gpt-4o-mini** sera alors disponible avec cette clé et le nombre de **tokens** sera **limité à 5000**.

```bash
export OPENAI_API_KEY=demo
```

## Déclarer les starters Spring Boot

La [documentation Spring Boot Integration](https://docs.langchain4j.dev/tutorials/spring-boot-integration) de LangChain4j explique comment les starters Spring Boot aident à configurer l’usage des larges modèles de langages, des embedding models et des embedding stores par le biais de propriétés à déclarer dans le fichier **application.properties** (ou application.yaml).

Dans le pom.xml de Spring Petclinic, commençons par déclarer les deux dépendances **langchain4j-spring-boot-starter** et **langchain4j-open-ai-spring-boot-starter** :

```xml
<properties>
  <langchain4j.version>0.35.0</langchain4j.version>
</properties>

<dependency>
  <groupId>dev.langchain4j</groupId>
  <artifactId>langchain4j-spring-boot-starter</artifactId>
  <version>${langchain4j.version}</version>
</dependency>
<dependency>
  <groupId>dev.langchain4j</groupId>
  <artifactId>langchain4j-open-ai-spring-boot-starter</artifactId>
  <version>${langchain4j.version}</version>
</dependency>
```

Le premier starter **langchain4j-spring-boot-starter** expose la classe d’auto-configuration pour Spring Boot [LangChain4jAutoConfig](https://github.com/langchain4j/langchain4j-spring/blob/3fbf707037689cda90f67dc02ca54983cfd1a5ce/langchain4j-spring-boot-starter/src/main/java/dev/langchain4j/spring/LangChain4jAutoConfig.java) et donne, entre autre, accès à l’annotation [@AiService](https://github.com/langchain4j/langchain4j-spring/blob/3fbf707037689cda90f67dc02ca54983cfd1a5ce/langchain4j-spring-boot-starter/src/main/java/dev/langchain4j/service/spring/AiService.java) que nous utiliserons dans une prochaine étape.

Le second starter **langchain4j-open-ai-spring-boot-starter** permet quant à lui de parser et binder les propriétés spécifiques à OpenAI du fichier de configuration application.properties (ex : _langchain4j.azure-open-ai.chat-model.api-key_). Par transitivité, il tire les artefacts langchain4j-open-ai et dev.ai4j:openai4j. En interne, LangChain4j s’appuie sur le **client Java non officiel** [**openai4j**](https://github.com/ai-for-java/openai4j) permettant de connecter des applications Java à l'API OpenAI.

## Configuration OpenAI

Dans une première version du chatbot ne faisant pas encore l’usage du streaming, ajouter au fichier [application.properties](https://github.com/spring-petclinic/spring-petclinic-langchain4j/blob/main/src/main/resources/application.properties) les 4 propriétés suivantes :

```properties
langchain4j.open-ai.chat-model.api-key=${OPENAI_API_KEY}
langchain4j.open-ai.chat-model.model-name=gpt-4o
langchain4j.open-ai.chat-model.log-requests=true
langchain4j.open-ai.chat-model.log-responses=true
```

Plus compact et moins cher que le **modèle gpt-4o** préconisé pour la démo, le modèle **gpt-4o-mini** peut également être utilisé et sait répondre aux exemples de questions suggérées dans le [readme.md](https://github.com/spring-petclinic/spring-petclinic-langchain4j/blob/main/readme.md).

Spring Boot détermine les beans à instancier en fonction des propriétés déclarées. A titre d’exemple, la classe [_AutoConfig_](https://github.com/langchain4j/langchain4j-spring/blob/main/langchain4j-open-ai-spring-boot-starter/src/main/java/dev/langchain4j/openai/spring/AutoConfig.java) du starter LangChain4j OpenAI pour Spring Boot, déclare conditionnellement un bean de type [_OpenAiChatModel_](https://github.com/langchain4j/langchain4j/blob/0.35.0/langchain4j-open-ai/src/main/java/dev/langchain4j/model/openai/OpenAiChatModel.java) implémentant l’interface agnostique [**_ChatLanguageModel_**](https://github.com/langchain4j/langchain4j/blob/0.35.0/langchain4j-core/src/main/java/dev/langchain4j/model/chat/ChatLanguageModel.java) lorsque la propriété _langchain4j.open-ai. **chat-model**.api-key_ est déclarée. Dans la suite de cet article, nous aurons besoin d’un bean de type [_StreamingChatLanguageModel_](https://github.com/langchain4j/langchain4j/blob/0.35.0/langchain4j-core/src/main/java/dev/langchain4j/model/chat/StreamingChatLanguageModel.java) permettant de streamer la réponse du LLM token par token.   
Sur le même principe, la propriété _langchain4j.open-ai. **streaming-chat-model**.api-key_ déclenchera l’instanciation d’un bean de type [_OpenAiStreamingChatModel_](https://github.com/langchain4j/langchain4j/blob/0.35.0/langchain4j-open-ai/src/main/java/dev/langchain4j/model/openai/OpenAiStreamingChatModel.java) implémentant l’interface _StreamingChatLanguageModel_.

## Déclarer un AI Service

Dans la suite de cet article, le code Java dédié au chatbot est localisé dans un package dédié : [org.springframework.samples.petclinic.chat](https://github.com/spring-petclinic/spring-petclinic-langchain4j/tree/main/src/main/java/org/springframework/samples/petclinic/chat).

Dans le code métier, l’interaction avec le LLM se fait au travers d’une simple interface Java nommée [**Assistant**](https://github.com/spring-petclinic/spring-petclinic-langchain4j/blob/main/src/main/java/org/springframework/samples/petclinic/chat/Assistant.java) et annotée avec l’annotation **@AiService**. LangChain4j propose un mécanisme similaire à Spring Data et Square Retrofit : on définit de manière déclarative une interface respectant des conventions de nommage et, au runtime, LangChain4j fournit une implémentation de cette interface. Se référer à la documentation [AI Services](https://docs.langchain4j.dev/tutorials/ai-services) pour davantage d’explications.  
L’interface Assistant propose une seule et unique méthode **chat**. Celle-ci accepte une question de l’utilisateur et renvoie la réponse du LLM sous forme de String.

```typescript
import dev.langchain4j.service.SystemMessage;
import dev.langchain4j.service.spring.AiService;

@AiService
interface Assistant {

    @SystemMessage(fromResource = "/prompts/system.st")
    String chat(String userMessage);

}
```

Le bean implémentant cette interface est mise à disposition par Spring et pourra être injecté, par exemple, dans le contrôleur REST.

## Prompter un Message Système

Pour répondre à l’utilisateur, nous **guidons le comportement du LLM** en définissant un « **system message** » via l’annotation **@SystemMessage**.  Les directives sont externalisées dans le fichier texte [system.st](https://github.com/spring-petclinic/spring-petclinic-langchain4j/blob/main/src/main/resources/prompts/system.st) :

```text
You are a friendly AI assistant designed to help with the management of a veterinarian pet clinic called Spring Petclinic.
Your job is to answer questions about and to perform actions on the user's behalf, mainly around
veterinarians, owners, owners' pets and owners' visits.
If you need access to pet owners or pet types, list and locate them without asking the user.
You are required to answer in a professional manner. If you don't know the answer, politely inform the user,
and then ask a follow-up question to help clarify what they are asking.
If you do know the answer, provide the answer but do not provide any additional followup questions.
When dealing with vets, if the user is unsure about the returned results, explain that there may be additional data that was not returned.
Only if the user is asking about the total number of all vets, answer that there are a lot and ask for some additional criteria.
For owners, pets or visits - provide the correct data.

```

Comme expliqué par Oded dans son [article de blog](https://spring.io/blog/2024/09/26/ai-meets-spring-petclinic-implementing-an-ai-assistant-with-spring-ai-part-i), le contexte système doit être régulièrement enrichi et optimisé afin que les réponses soient les plus précises et les plus fiables possibles.  
Par exemple, afin que le LLM prenne des initiatives sans demander l’aval de l’utilisateur, le message système a été récemment complété avec la directive suivante :

```batch
If you need access to pet owners or pet types, list and locate them without asking the user.
```

Sans cette directive, le LLM demande l’autorisation de rechercher l’ID de Betty :

{{< figure src="/wp-content/uploads/2024/11/chat0.png" alt="" caption="" >}}

## Déclarer un contrôleur REST

Le chabot est appelé depuis le navigateur via une API REST. Déclarer un contrôleur Rest [AssistantController](https://github.com/spring-petclinic/spring-petclinic-langchain4j/blob/main/src/main/java/org/springframework/samples/petclinic/chat/AssistantController.java) exposant le **endpoint _/chat_**:

```java
@RestController
class AssistantController {

    private final Assistant assistant;

    AssistantController(Assistant assistant) {
       this.assistant = assistant;
    }

    @PostMapping("/chat")
    public String chat(@RequestBody String query) {
       return assistant.chat(query);
    }

}
```

Démarrer l’application Spring Boot et vérifier le fonctionnement du chatbot via un simple appel curl :

{{< figure src="/wp-content/uploads/2024/11/curl1.png" alt="" caption="" >}}

## Paramétrer la mémoire conversationnelle de l’assistant

A ce stade, le chatbot n’a pas encore de mémoire. Il ne peut donc pas s’aider des précédents échanges pour générer une réponse. Voici un des exemples des plus connus :

{{< figure src="/wp-content/uploads/2024/11/curl2.png" alt="" caption="" >}}

Pour remédier à ce problème, nous déclarons un bean Spring de type [**ChatMemory**](https://docs.langchain4j.dev/tutorials/ai-services#chat-memory) qui conserve l’ **historique des 10 derniers messages**.

```java
@Configuration
class AssistantConfiguration {

    @Bean
    ChatMemory chatMemory() {
       return MessageWindowChatMemory.withMaxMessages(10);
    }

}
```

Le prénom donné lors du premier appel est désormais réutilisé par le LLM lors du deuxième appel :

{{< figure src="/wp-content/uploads/2024/11/curl3.png" alt="" caption="" >}}

Par défaut, les messages sont sauvegardés en mémoire dans un [InMemoryChatMemoryStore](https://github.com/langchain4j/langchain4j/blob/aa0e48816657640eda75879f1c29c0348643575c/langchain4j-core/src/main/java/dev/langchain4j/store/memory/chat/InMemoryChatMemoryStore.java#L15). En cas de **redémarrage** de l’application, les messages volatiles sont perdus. Avec **plusieurs instances** de la même application sans affinité de sessions, l’historique des messages est réparti sur différentes JVM. Cela pose également problème. Une solution consiste à implémenter l’interface [ChatMemoryStore](https://github.com/langchain4j/langchain4j/blob/0.35.0/langchain4j-core/src/main/java/dev/langchain4j/store/memory/chat/ChatMemoryStore.java) afin de **persister les messages** en base ou dans un cache distribué. Se référer à l’exemple [ServiceWithPersistentMemoryForEachUserExample.java](https://github.com/langchain4j/langchain4j-examples/blob/main/other-examples/src/main/java/ServiceWithPersistentMemoryForEachUserExample.java).

## Supporter plusieurs utilisateurs

A ce stade, la même instance de _ChatMemory_ est utilisée pour toutes les invocations du service d'IA. Cette approche a des limites et ne fonctionnera pas avec plusieurs utilisateurs. Chaque utilisateur a besoin de sa propre instance de _ChatMemory_ pour maintenir sa conversation individuelle.  
Une [solution proposée par LangChain4j](https://docs.langchain4j.dev/tutorials/ai-services/#chat-memory) consiste à utiliser un [**ChatMemoryProvider**](https://github.com/langchain4j/langchain4j/blob/0.35.0/langchain4j/src/main/java/dev/langchain4j/memory/chat/ChatMemoryProvider.java) :

```java
@Configuration
class AssistantConfiguration {

	@Bean
	ChatMemoryProvider chatMemoryProvider() {
		return memoryId -> MessageWindowChatMemory.withMaxMessages(10);
	}
}
```

Chaque utilisateur est associé à un **memoryId** qui lui est dédié et dispose donc de sa propre ChatMemory.

La signature de la méthode _chat_ de l’interface _Assistant_ prend désormais un second paramètre nommé memoryId, annoté avec l’annotation [**@MemoryId**](https://github.com/langchain4j/langchain4j/blob/main/langchain4j/src/main/java/dev/langchain4j/service/MemoryId.java) et de type UUID v4. Le paramètre userMessage est quant à lui annoté avec [**@UserMessage**](https://github.com/langchain4j/langchain4j/blob/0.35.0/langchain4j/src/main/java/dev/langchain4j/service/UserMessage.java) :

```typescript
import dev.langchain4j.service.MemoryId;
import dev.langchain4j.service.SystemMessage;
import dev.langchain4j.service.spring.AiService;

@AiService
interface Assistant {

    @SystemMessage(fromResource = "/prompts/system.st")
    String chat(@MemoryId UUID memoryId, @UserMessage String userMessage);

}
```

Le contrôleur REST est adapté en fonction :

```java
@PostMapping(value = "/chat/{user}")
public String chat(@PathVariable UUID user, @RequestBody String query) {

    return assistant.chat(user, query);
}
```

La [Pull Request #8 Support multiple users with @MemoryId](https://github.com/spring-petclinic/spring-petclinic-langchain4j/pull/8) montre un exemple d’illustration côté frontend.

## Ajouter un widget de chat

L’ **interface web** du chat a été [designée par Oded](https://spring.io/blog/2024/09/27/ai-meets-spring-petclinic-implementing-an-ai-assistant-with-spring-ai-part#implementing-the-ui). Les codes HTML, JavaScript et CSS sont respectivement localisés dans les fichiers [layout.html](https://github.com/spring-petclinic/spring-petclinic-langchain4j/blob/main/src/main/resources/templates/fragments/layout.html) et [chat.js](https://github.com/spring-petclinic/spring-petclinic-langchain4j/blob/main/src/main/resources/static/resources/js/chat.js) et [chat.css](https://github.com/spring-petclinic/spring-petclinic-langchain4j/blob/main/src/main/resources/static/resources/css/chat.css)

Certaines réponses d’ **OpenAI** sont formattés en **Markdown**.  
Côté front, la librairie [**MarkedJS**](https://marked.js.org/) permet de convertir le markdown en HTML. Elle est ajoutée dans la configuration maven en tant que webjar :

```xml
<dependency>
  <groupId>org.webjars.npm</groupId>
  <artifactId>marked</artifactId>
  <version>${webjars-marked.version}</version>
</dependency>
```

## Ajouter une première fonction

Afin d’interagir avec le code métier de l’application, les développeurs peuvent proposer aux LLM d’appeler des fonctions, en l’occurrence du code Java. L'appel de fonctions personnalisées renforce la capacité des LLM à fournir des réponses plus pertinentes et contextuelles. Le LLM peut, par exemple, **accéder aux données de l’application**.  
Le LLM n’appelle pas directement les fonctions : **le modèle produit une sortie de données structurées qui spécifie le nom de la fonction** à appeler ainsi que les **arguments suggérés**. Les fonctions sont appelées par l’application Java ayant appelée le LLM.  
A noter que tous les LLM ne supportent pas encore l’appel de fonctions.

LangChain4j facilite et standardise l’ **appel de fonctions** via les [**Tools**](https://docs.langchain4j.dev/tutorials/tools). Deux niveaux d’abstraction sont proposés :

1. **Low-level**, en utilisant la classe [ToolSpecification](https://github.com/langchain4j/langchain4j/blob/0.35.0/langchain4j-core/src/main/java/dev/langchain4j/agent/tool/ToolSpecifications.java) pour décrire les fonctions au LLM : nom, description, paramètres d’entrée / sortie.
1. **High-level**, à l'aide des services d’IA et des méthodes Java annotées [**@Tool**](https://github.com/langchain4j/langchain4j/blob/0.35.0/langchain4j-core/src/main/java/dev/langchain4j/agent/tool/Tool.java)

Nous mettrons en œuvre celui de haut niveau permettant d’annoter n'importe quelle méthode Java avec l'annotation [**@Tool**](https://github.com/langchain4j/langchain4j/blob/0.35.0/langchain4j-core/src/main/java/dev/langchain4j/agent/tool/Tool.java). LangChain4j génère automatiquement les [ToolSpecification](https://github.com/langchain4j/langchain4j/blob/0.35.0/langchain4j-core/src/main/java/dev/langchain4j/agent/tool/ToolSpecifications.java) s à partir de la signature des méthodes annotées.  Lors de l’appel du LLM, la description des fonctions qui sont mises à sa disposition lui sont transmises. Lorsque le LLM décide d’appeler une fonction, LangChain4j exécute automatiquement la méthode Java appropriée et sa valeur de retour est renvoyée au LLM. Sous la forme d’un simple bean Spring, la classe [**AssistantTool**](https://github.com/spring-petclinic/spring-petclinic-langchain4j/blob/main/src/main/java/org/springframework/samples/petclinic/chat/AssistantTool.java) expose les fonctions que le LLM pourra invoquer pour récupérer des données de référence, lister les propriétaires ou bien encore ajouter en base un animal de compagnie. Commençons par déclarer une function nommée **getAllOwners** :

```java
@Component
public class AssistantTool {

    private final OwnerRepository ownerRepository;

    public AssistantTool(OwnerRepository ownerRepository) {
       this.ownerRepository = ownerRepository;
    }

    @Tool("List the owners that the pet clinic has: ownerId, name, address, phone number, pets")
    public OwnersResponse getAllOwners() {
       Pageable pageable = PageRequest.of(0, 100);
       Page<Owner> ownerPage = ownerRepository.findAll(pageable);
       return new OwnersResponse(ownerPage.getContent());
    }

}

record OwnersResponse(List<Owner> owners) {
}
```

En interne, la classe _AssistantTool_ utilise le repository Spring Data JPA [OwnerRepository](https://github.com/spring-petclinic/spring-petclinic-langchain4j/blob/main/src/main/java/org/springframework/samples/petclinic/owner/OwnerRepository.java) utilisé par l’application.  
Apposée au niveau de l’annotation @Tool, **la description aide le LLM à comprendre quand appeler la fonction**.  
La fonction _getAllOwners()_ ne prend pas de paramètre. Elle retourne le record _OwnersResponse_ qui contient une liste de _Owner_. La classe Owner est une entité JPA existante et utilisée pour l’IHM. Cet exemple démontre donc les capacités de LangChain4j à réutiliser le code existant.  
Une fois la fonction appelée, LangChain4j convertit le record _OwnersResponse_ au format JSON pour que le LLM puisse le traiter.

A noter que la méthode _getAllOwners_ n’aurait pas sa place dans une application d’entreprise. L’application démo Spring Petclinic compte seulement 10 propriétaires. Renvoyer toutes les données de la base ne pose donc pas de problème de performance. Néanmoins, dans une vraie application de gestion, **proposer une méthode de recherche multi-critères serait préférable**. C’est ce que propose l’ [issue #9](https://github.com/spring-petclinic/spring-petclinic-langchain4j/issues/9).

Interrogeons à présent le chatbot avec la question _« Please list the owners that come to the clinic. »_ et regardons le flux d’échange entre l’application Petclinic et OpenAI.

{{< figure src="/wp-content/uploads/2024/11/chat1.png" alt="" caption="" >}}

Au préalable, dans le fichier _application.properties_, nous avons activé les logs des requêtes et réponses envoyées à OpenAI :

```properties
langchain4j.open-ai.chat-model.log-requests=true
langchain4j.open-ai.chat-model.log-responses=true
```

Lors du 1er appel à OpenAI, à côté de la question saisie par l’utilisateur dans le fenêtre de chat, la fonction _getAllOwners_ est proposée dans une liste de tools.

Log partiel de la requête #1 :

```text
- method: POST
- url: https://api.openai.com/v1/chat/completions
- headers: [Authorization: Bearer xxxx], [User-Agent: langchain4j-openai]
- body: {
  "model" : "gpt-4o",
  "messages" : [ {
    "role" : "system",
    "content" : "You are a friendly AI assistant designed to help with the management of a veterinarian pet clinic called Spring Petclinic…"
  }, {
    "role" : "user",
    "content" : "\"Please list the owners that come to the clinic.\"
} ],
  "temperature" : 0.7,
  "tools" : [{
    "type" : "function",
    "function" : {
      "name" : "getAllOwners",
      "description" : "List the owners that the pet clinic has: ownerId, name, address, phone number, pets",
      "parameters" : {
        "type" : "object",
        "properties" : { },
        "required" : [ ]
      }
    }
  }, …

```

Comme attendu, OpenAI demande à l’application d’appeler la function _getAllOwners_.  
Log partiel de la réponse #1 :

```text
status code: 200
- headers: xxxx
- body: {
  "id": "chatcmpl-AOqizmPVZnGZ9jAB2of6NhayYi2mY",
  "object": "chat.completion",
  "created": 1730485909,
  "model": "gpt-4o-2024-08-06",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": null,
        "tool_calls": [
          {
            "id": "call_6fe84CTFo3zwOvo10ZBgBqjl",
            "type": "function",
            "function": {
              "name": "getAllOwners",
              "arguments": "{}"
            }
          }
        ],
…. }
```

LangChain4j fait aussitôt appel à la méhtode **_getAllOwners_** du bean _AssistantTool_. Le résultat est sérialisé en JSON et placé dans l’attribut **content** lors du second appel au LLM.

Log partiel de la requête #2 :

```text
- method: POST
- url: https://api.openai.com/v1/chat/completions
- headers: [Authorization: Bearer sk-Qw...MA], [User-Agent: langchain4j-openai]
- body: {
  "model" : "gpt-4o",
  "messages" : [ {
    "role" : "system",
    "content" : "You are a friendly AI …"
  }, {
    "role" : "user",
    "content" : "\"Please list the owners that come to the clinic"
  }, {
    "role" : "assistant",
    "tool_calls" : [ {
      "id" : "call_6fe84CTFo3zwOvo10ZBgBqjl",
      "type" : "function",
      "function" : {
        "name" : "getAllOwners",
        "arguments" : "{}"
      }
    } ]
  }, {
    "role" : "tool",
    "tool_call_id" : "call_6fe84CTFo3zwOvo10ZBgBqjl",
    "content" : "{\n  \"owners\": [\n    {\n      \"address\": \"110 W. Liberty St.\",\n      \"city\": \"Madison\",\n      \"telephone\": \"6085551023\",\n      \"pets\": [\n        {\n          \"birthDate\": \"2010-09-07\",\n          \"type\": {\n            \"name\": \"cat\",\n            \"id\": 1\n          },\n          \"visits\": [],\n          \"name\": \"Leo\",\n          \"id\": 1\n        }\n      ],\n      \"firstName\": \"George\",\n      \"lastName\": \"Franklin\",\n      \"id\": 1\n    },\n    {\n      \"address\": \"638 Cardinal Ave.\",\n      \"city\": \"Sun Prairie\",\n      \"telephone\": \"6085551749\",\n      \"pets\": [\n        {\n          \"birthDate\": \"2012-08-06\",\n          \"type\": {\n            \"name\": \"hamster\",\n            \"id\": 6\n          },\n          \"visits\": [],\n          \"name\": \"Basil\",\n          \"id\": 2\n        }\n      ],\n      \"firstName\": \"Betty\",\n      \"lastName\": \"Davis\",\n      \"id\": 2\n,   …
  } ],
  "temperature" : 0.7,
  "tools" : [ { …}]

```

OpenAI utilise le résultat de l’appel à la fonction _getAllOwners_ pour générer une réponse présentant une liste de propriétaires d’animaux formatée en markdown :

Log partiel de la réponse #2 :

```text
- status code: 200
- headers: …
- body: {
  "id": "chatcmpl-AOqj0Y9yhJjzYtzV7QMXiBU4URkJ7",
  "object": "chat.completion",
  "created": 1730485910,
  "model": "gpt-4o-2024-08-06",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Here is a list of the owners at the Spring Petclinic:\n\n1. **George Franklin**\n   - Address: 110 W. Liberty St., Madison\n   - Telephone: 6085551023\n   - Pets: \n     - Leo (Cat, born on 2010-09-07)\n\n2. **Betty Davis**\n   - Address: 638 Cardinal Ave., Sun Prairie\n   - Telephone: 6085551749\n   - Pets: \n     - Basil (Hamster, born on 2012-08-06)\n\n3. **Eduardo Rodriquez**\n   - Address: 2693 Commerce St., McFarland\n   - Telephone: 6085558763\n   - Pets: \n     - Jewel (Dog, born on 2010-03-07)\n     - Rosy (Dog, born on 2011-04-17)\n\n4. **Harold Davis**\...",
        …
    }
  ],
  "usage": { … }

```

Cette première fonction a montré comment le LLM peut récupérer des données depuis la base de données pour générer sa réponse.

## Agent conversationnel

Ajoutons à présent les fonctions permettant à un vétérinaire de déclarer un nouvel animal de compagnie pour l’un de ses clients, en formulant dans le chat la requête suivante :

> _Add a dog for Betty Davis. His name is Moopsie. His birthday is on 2 October 2024._
>
> {{< figure src="/wp-content/uploads/2024/11/agent-question.png" alt="" caption="" >}}

Dans la classe _AssistantTool_, ajoutons une seconde fonction _addPetToOwner_ permettant à un vétérinaire de déclarer un nouvel animal de compagnie à l’un de ses clients :

```java
@Tool("Add a pet with the specified petTypeId, to an owner identified by the ownerId")
public AddedPetResponse addPetToOwner(AddPetRequest request) {
    Owner owner = ownerRepository.findById(request.ownerId());
    owner.addPet(request.pet());
    this.ownerRepository.save(owner);
    return new AddedPetResponse(owner);
}
```

Cette fois-ci, la méthode accepte un paramètre de type [AddPetRequest](https://github.com/spring-petclinic/spring-petclinic-langchain4j/blob/f03f5ae28c2a0d7575fb61ce77ad74b74035ffea/src/main/java/org/springframework/samples/petclinic/chat/AssistantTool.java#L72) :

```java
record AddPetRequest(Pet pet, Integer ownerId) {
}
```

Pour ajouter un animal de compagnie, le LLM doit connaitre l’identifiant du propriétaire (le _ownerId_) et les données caractérisant son compagnon. Cet identifiant peut être récupéré par le LLM via l’appel de la fonction _getAllOwners_.  
Le LLM doit également savoir comment valoriser les attributs de la classe [Pet](https://github.com/spring-petclinic/spring-petclinic-langchain4j/blob/f03f5ae28c2a0d7575fb61ce77ad74b74035ffea/src/main/java/org/springframework/samples/petclinic/owner/Pet.java) : _name_, _birthDate_, _visits_ et _type_. Les identifiants du type [PetType](https://github.com/spring-petclinic/spring-petclinic-langchain4j/blob/f03f5ae28c2a0d7575fb61ce77ad74b74035ffea/src/main/java/org/springframework/samples/petclinic/owner/PetType.java) (ex : 1=cat, 2=dog …) peuvent être listés par le LLM via l’appel de la nouvelle fonction _populatePetTypes_ :

```java
@Tool("List all pairs of petTypeId and pet type name")
public List<PetType> populatePetTypes() {
    return this.ownerRepository.findPetTypes();
}
```

Lorsque OpenAI est interrogé, dans sa première réponse, il demande à LangChain4j d’appeler 2 fonctions / tools. Optimisé, cela évitera les allers-retours :

Log partiel de la réponse #1 :

```text
2024-11-02T18:14:50.532+01:00 DEBUG 10650 --- [.openai.com/...] d.a.openai4j.StreamingRequestExecutor    : onEvent() {"id":"chatcmpl-APC01s26BWq4QFXC1tpIgHuSml798","object":"chat.completion.chunk","created":1730567689,"model":"gpt-4o-2024-08-06","system_fingerprint":"fp_159d8341cc","usage":null,"choices":[{"index":0,"delta":{"tool_calls":[{"index":0,"id":"call_T0QYuwvX9NGD6kX9KxFLKrDm","type":"function","function":{"name":"getAllOwners","arguments":""}}]},"logprobs":null,"finish_reason":null}]}
2024-11-02T18:14:50.534+01:00 DEBUG 10650 --- [.openai.com/...] d.a.openai4j.StreamingRequestExecutor    : onEvent() {"id":"chatcmpl-APC01s26BWq4QFXC1tpIgHuSml798","object":"chat.completion.chunk","created":1730567689,"model":"gpt-4o-2024-08-06","system_fingerprint":"fp_159d8341cc","usage":null,"choices":[{"index":0,"delta":{"tool_calls":[{"index":1,"id":"call_hRf3HX1yLDIU0DtAr5Sjmov5","type":"function","function":{"name":"populatePetTypes","arguments":""}}]},"logprobs":null,"finish_reason":null}]}
2024-11-02T18:14:50.534+01:00 DEBUG 10650 --- [.openai.com/...] d.a.openai4j.StreamingRequestExecutor    : onEvent() {"id":"chatcmpl-APC01s26BWq4QFXC1tpIgHuSml798","object":"chat.completion.chunk","created":1730567689,"model":"gpt-4o-2024-08-06","system_fingerprint":"fp_159d8341cc","usage":null,"choices":[{"index":0,"delta":{"tool_calls":[{"index":1,"function":{"arguments":"{}"}}]},"logprobs":null,"finish_reason":null}]}
```

LangChain4j appelle séquentiellement ces 2 fonctions (paralléliser ces appels serait un axe d’optimisation de notre application : [issue #13](https://github.com/spring-petclinic/spring-petclinic-langchain4j/issues/13)) puis renvoie les résultats à OpenAI.

Log partiel de la requête #2 :

```json
  "tool_calls" : [ {
      "id" : "call_T0QYuwvX9NGD6kX9KxFLKrDm",
      "type" : "function",
      "function" : {
        "name" : "getAllOwners",
        "arguments" : "{}"
      }
    }, {
      "id" : "call_hRf3HX1yLDIU0DtAr5Sjmov5",
      "type" : "function",
      "function" : {
        "name" : "populatePetTypes",
        "arguments" : "{}"
      }
    } ]
  }, {
    "role" : "tool",
    "tool_call_id" : "call_T0QYuwvX9NGD6kX9KxFLKrDm",
    "content" : "{\n  \"owners\": [\n    {\n      \"address\": \"638 Cardinal Ave.\",\n      \"city\": \"Sun Prairie\",\n      \"telephone\": \"6085551749\",\n      \"pets\": [\n        {\n          \"birthDate\": \"2012-08-06\",\n          \"type\": {\n            \"name\": \"hamster\",\n            \"id\": 6\n          },\n          \"visits\": [],\n          \"name\": \"Basil\",\n          \"id\": 2\n        }\n      ],\n      \"firstName\": \"Betty\",\n      \"lastName\": \"Davis\",\n      \"id\": 2\n    }, …\]\n}"
  }, {
    "role" : "tool",
    "tool_call_id" : "call_hRf3HX1yLDIU0DtAr5Sjmov5",
    "content" : "[\n  {\n    \"name\": \"bird\",\n    \"id\": 5\n  },\n  {\n    \"name\": \"cat\",\n    \"id\": 1\n  },\n  {\n    \"name\": \"dog\",\n    \"id\": 2\n  },\n  {\n    \"name\": \"hamster\",\n    \"id\": 6\n  },\n  {\n    \"name\": \"lizard\",\n    \"id\": 3\n  },\n  {\n    \"name\": \"snake\",\n    \"id\": 4\n  }\n]"
  } ],

```

De ces 2 appels de fonctions, OpenAI déduit l’identifiant de Betty Davis égal à 2 ainsi que l’identifiant d’un chien lui aussi égal à 2. En réponse, il demande à LangChain4j d’appeler la fonction _addPetToOwner_ en lui passant ces deux identifiants, ainsi que le nom et la date de naissance donné par l’utilisateur.

```text
2024-11-02T18:14:51.734+01:00 DEBUG 10650 --- [.openai.com/...] d.l.service.tool.DefaultToolExecutor     : About to execute ToolExecutionRequest { id = "call_7TdLNNZPsMD4ujev8wRytdyf", name = "addPetToOwner", arguments = "{"request":{"ownerId":2,"pet":{"name":"Moopsie","birthDate":{"year":2024,"month":10,"day":2},"type":{"id":2}}}}" } for memoryId 510e5396-3c19-46c2-991c-3200a653f90f
2024-11-02T18:14:51.798+01:00 DEBUG 10650 --- [.openai.com/...] d.l.service.tool.DefaultToolExecutor     : Tool execution result: {
  "owner": {
    "address": "638 Cardinal Ave.",
    "city": "Sun Prairie",
    "telephone": "6085551749",
    "pets": [
      {
        "birthDate": "2012-08-06",
        "type": {
          "name": "hamster",
          "id": 6
        },
        "visits": [],
        "name": "Basil",
        "id": 2
      },
      {
        "birthDate": "2024-10-02",
        "type": {
          "id": 2
        },
        "visits": [],
        "name": "Moopsie"
      }
    ],
    "firstName": "Betty",
    "lastName": "Davis",
    "id": 2
  }
}
```

Cette fois-ci, LangChain4j doit passer un paramètre de type _AddPetRequest_ lors de l’appel à la fonction _addPetToOwner_. La structure de donnée a préalablement été communiquée au LLM lors de la description de la fonction mise à sa disposition :

```json
{
  "type": "function",
  "function": {
    "name": "addPetToOwner",
    "description": "Add a pet with the specified petTypeId, to an owner identified by the ownerId",
    "parameters": {
      "type": "object",
      "properties": {
        "request": {
          "type": "object",
          "properties": {
            "ownerId": {
              "type": "integer"
            },
            "pet": {
              "type": "object",
              "properties": {
                "visits": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "date": {
                        "type": "object",
                        "properties": {
                          "month": {
                            "type": "integer"
                          },
                          "year": {
                            "type": "integer"
                          },
                          "day": {
                            "type": "integer"
                          }
                        },
                        "required": []
                      },
                      "description": {
                        "type": "string"
                      }
                    },
                    "required": []
                  }
                },
                "type": {
                  "type": "object",
                  "properties": {},
                  "required": []
                },
                "birthDate": {
                  "type": "object",
                  "properties": {
                    "month": {
                      "type": "integer"
                    },
                    "year": {
                      "type": "integer"
                    },
                    "day": {
                      "type": "integer"
                    }
                  },
                  "required": []
                }
              },
              "required": []
            }
          },
          "required": []
        }
      },
      "required": [
        "request"
      ]
    }
  }
}
```


**Le LLM a structuré en JSON les paramètres d’appel de fonction**. La classe [DefaultToolExecutor](https://github.com/langchain4j/langchain4j/blob/0.35.0/langchain4j/src/main/java/dev/langchain4j/service/tool/DefaultToolExecutor.java) de LangChain4j se charge d’unmarshaller les données JSON. En interne, elle s’appuie sur une librairie JSON (à termes, Jackson doit remplacer Google GSON).

Les résultats des 3 appels de fonction sont renvoyés à OpenAI dans une 3ième et dernière requête. Ce dernier conclue que l’ajout s’est bien passé et récapitule les informations enregistrées.

Voici un **diagramme de séquences** illustrant les appels que nous venons de décrire :

{{< figure src="/wp-content/uploads/2024/11/LangChain4j-addPetToOwner.png" alt="" caption="" >}}

##   
Response Streaming

La méthode _chat()_ déclarée dans le _@AiService_ renvoie une simple _String_. L’utilisateur doit attendre que le LLM ait généré l’intégralité de sa réponse avant de recevoir le résultat. Ceci est regrettable lorsqu’on sait qu’un LLM génère du texte un jeton à la fois.  
La plupart des LLM propose un moyen de **diffuser la réponse jeton par jeton** au lieu d'attendre que l'ensemble du texte soit généré. Cette possibilité améliore l'expérience de l'utilisateur qui n'a alors pas besoin d'attendre une durée inconnue et peut commencer à lire la réponse presque immédiatement. LangChain4j supporte nativement cette [fonctionnalité de **Response Streaming**](https://docs.langchain4j.dev/tutorials/ai-services#streaming). Il sait streamer token par token en utilisant l’interface [TokenStream](https://github.com/langchain4j/langchain4j/blob/main/langchain4j/src/main/java/dev/langchain4j/service/TokenStream.java) comme type de réponse. Le client peut s’abonner aux flux de jetons renvoyé par le LLM et ainsi être notifié lorsqu’un nouveau jeton est disponible. Modifions la signature de notre méthode :

```typescript
interface Assistant {

    @SystemMessage(fromResource = "/prompts/system.st")
    TokenStream chat(@MemoryId UUID memoryId, @UserMessage String userMessage);

}
```

Remarque : cette version de l’application Spring Petclinic est développée sur une stack non réactive avec Spring MVC. Si elle l’avait été avec Spring Webflux, nous aurions pu utiliser le type **_Flux<String>_** à la place de _TokenStream_.

Le contrôleur REST [AssistantController](https://github.com/spring-petclinic/spring-petclinic-langchain4j/blob/v3.3.3/src/main/java/org/springframework/samples/petclinic/chat/AssistantController.java) doit à son tour être adapté. De la même manière que sur l’application web ChatGPT, nous utilisons la technologie **Server Sent Events** (SSE) pour que le serveur envoie au navigateur au fil de l’eau les réponses du LLM. Spring Framework supporte nativement SSE depuis 2015 via la classe **SseEmitter**, se référer à sa [documentation](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-async.html#mvc-ann-async-sse).

Chaque token est envoyé dans un message structuré en JSON. L’onglet EventStream de Google Chrome donne un aperçu du résultat :

{{< figure src="/wp-content/uploads/2024/11/event-stream-chrome.png" alt="" caption="" >}}

Dans le contrôleur, l’appel à la méthode _chat()_ est fait en asynchrone par un ExecutorService. L’appelant n’est pas bloqué. L’envoie des tokens au client (dans notre cas au navigateur) est assuré par l’appel à la classe SseEmitter.

```java
@RestController
class AssistantController {

    private static final Logger LOGGER = LoggerFactory.getLogger(AssistantController.class);

    private final Assistant assistant;

    private final ExecutorService nonBlockingService = Executors.newCachedThreadPool();

    AssistantController(Assistant assistant) {
       this.assistant = assistant;
    }

    // Using the POST method due to chat memory capabilities
    @PostMapping(value = "/chat/{user}")
    public SseEmitter chat(@PathVariable UUID user, @RequestBody String query) {
       SseEmitter emitter = new SseEmitter();
       nonBlockingService.execute(() -> assistant.chat(user, query).onNext(message -> {
          try {
             sendMessage(emitter, message);
          }
          catch (IOException e) {
             LOGGER.error("Error while writing next token", e);
             emitter.completeWithError(e);
          }
       }).onComplete(token -> emitter.complete()).onError(error -> {
          LOGGER.error("Unexpected chat error", error);
          try {
             sendMessage(emitter, error.getMessage());
          }
          catch (IOException e) {
             LOGGER.error("Error while writing next token", e);
          }
          emitter.completeWithError(error);
       }).start());
       return emitter;
    }

    private static void sendMessage(SseEmitter emitter, String message) throws IOException {
       String token = message
          // Hack line break problem when using Server Sent Events (SSE)
          .replace("\n", "<br>")
          // Escape JSON quotes
          .replace("\"", "\\\"");
       emitter.send("{\"t\": \"" + token + "\"}");
    }

}
```

A noter un hack (issue [#12](https://github.com/spring-petclinic/spring-petclinic-langchain4j/issues/12)) remplaçant les sauts de ligne du LLM pour pallier au [problème connu des sauts de lignes avec SSE](https://medium.com/@thiagosalvatore/the-line-break-problem-when-using-server-sent-events-sse-1159632d09a0).

En interne, pour streamer la réponse du LLM, LangChain4j utilise l’interface [StreamingChatLanguageModel](https://github.com/langchain4j/langchain4j/blob/0.35.0/langchain4j-core/src/main/java/dev/langchain4j/model/chat/StreamingChatLanguageModel.java) (à la place de ChatLanguageModel). Dans le fichier de configuration [application.properties](https://github.com/spring-petclinic/spring-petclinic-langchain4j/blob/v3.3.3/src/main/resources/application.properties), les propriétés langchain4j.open-ai. **chat-model**.xxx sont renommées en langchain4j.open-ai. **streaming-chat-model**.xxx :

```properties
langchain4j.open-ai.streaming-chat-model.api-key=${OPENAI_API_KEY}
langchain4j.open-ai.streaming-chat-model.model-name=gpt-4o
langchain4j.open-ai.streaming-chat-model.log-requests=true
langchain4j.open-ai.streaming-chat-model.log-responses=true
```

Côté front, le code JavaScript du fichier [chat.js](https://github.com/spring-petclinic/spring-petclinic-langchain4j/blob/v3.3.3/src/main/resources/static/resources/js/chat.js#L58) a été adapté pour accepter le type MIME **text/event-stream** et parser les messages JSON.

La [Pull Request #3 Response Streaming and SSE](https://github.com/spring-petclinic/spring-petclinic-langchain4j/pull/3) décrit tous les changements appliqués côté back et front pour passer au mode streaming.

## Retrieval Augmented Generation (RAG)

L’ensemble des tools mis à disposition du LLM par Petclinic lui permettent d’accéder aux données des propriétaires, de leurs animaux et de leurs visites. Rien sur les vétérinaires officiant dans la clinique. Afin de permettre aux utilisateurs de poser des questions sur les vétérinaires, nous allons exploiter une autre fonctionnalité majeure des LLM et de LangChain4j : la **génération augmentée par récupération**, connue en anglais sous l’acronyme RAG pour Retrieval Augmented Generation. Un RAG permet de fournir à un LLM des informations complémentaires dont il pourrait avoir besoin pour répondre aux requêtes des utilisateurs, en particulier lorsqu'il s'agit de données plus récentes ou de **contenus privés non accessibles lors de son entraînement**.  
Un RAG permet d’utiliser la recherche sémantique. Par exemple, dans la question suivante, l’utilisateur utilise des synonymes des spécialités déclarées en base de données dans le référentiel : radiography (radiographie) pour radiology (radiologue) et odontology (odontologie) pour dentistry (dentiste).

> Question : « I'm looking for a veterinarian who specializes in both radiography and odontology for my pet »

A l’aide du RAG, l’application Petclinic retrouve 2 vétérinaires ayant la spécialité de radiology et de dentistry. L’utilisation d’un index inversé Lucene n’aurait pas permis d’arriver à ce résultat.

{{< figure src="/wp-content/uploads/2024/11/langchain4j-question-llm.png" alt="" caption="" >}}

Pour intégrer le RAG à Petclinic, nous devons procéder en 2 étapes : la phase d’ **ingestion (indexation)** des vétérinaires et la phase de **requêtage** (retrieval en anglais). La [documentation de LangChain4j sur le support des RAG](https://docs.langchain4j.dev/tutorials/rag) propose deux diagrammes illustrant les étapes d’ [indexation](https://docs.langchain4j.dev/tutorials/rag#indexing) et de [retrieval](https://docs.langchain4j.dev/tutorials/rag#retrieval).

## Ingestion d’embeddings

Afin de pouvoir être utilisées par le LLM, les données des 3 tables _vets_, _specialties_ et _vet\_specialties_ doivent préalablement être ingérées et stockées dans une base de données vectorielle. PostgreSQL avec l'extension [pgVector](https://github.com/pgvector/pgvector) est probablement le choix le plus populaire. Greenplum et Qdrant sont 2 autres bases de données vectorielles. [LangChain4j supporte plus de 25 bases vectorielles](https://docs.langchain4j.dev/integrations/embedding-stores/) avec des niveaux plus ou moins avancés.

Lors de la phase d’ingestion, les données textuelles des vétérinaires (nom, prénom et spécialités) sont converties en vecteurs multidimensionnels appelés **embedding** puis stockés dans la base vectorielle. La documentation de LangChain4j parle **d’Embedding Stores**. Pour notre application d’exemple, par simplicité, nous allons utiliser la [base vectorielle en mémoire proposée par LangChain4j](https://docs.langchain4j.dev/integrations/embedding-stores/in-memory). Dans la classe de configuration Spring [AssistantConfiguration](https://github.com/spring-petclinic/spring-petclinic-langchain4j/blob/v3.3.3/src/main/java/org/springframework/samples/petclinic/chat/AssistantConfiguration.java), commençons par déclarer le bean de type [InMemoryEmbeddingStore](https://docs.langchain4j.dev/integrations/embedding-stores/in-memory) :

```java
@Bean
InMemoryEmbeddingStore<TextSegment> embeddingStore() {
    return new InMemoryEmbeddingStore<>();
}
```


Nous devons ensuite choisir un modèle de embedding. [LangChain4j en supporte plus de 19](https://docs.langchain4j.dev/category/embedding-models). J’ai opté pour un [modèle de type in-process](https://docs.langchain4j.dev/integrations/embedding-models/in-process) basé sur le runtime [ONNX](https://onnxruntime.ai/docs/get-started/with-java.html). Ce type de modèle présente l’avantage de pouvoir s’exécuter dans la même JVM que celle de Petclinic.  
Le repo git [langchain4j-embeddings](https://github.com/langchain4j/langchain4j-embeddings) propose une douzaine d’artefact (JAR) embarquant chacun un modèle au f **ormat .onnx**. Parmi eux, on retrouve l’artefact [langchain4j-embeddings-all-minilm-l6-v2](https://github.com/langchain4j/langchain4j-embeddings/tree/main/langchain4j-embeddings-all-minilm-l6-v2).

Le modèle [**all-MiniLM-L6-v2**](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) est un modèle de langage basé sur la famille [MiniLM](https://github.com/microsoft/unilm/tree/master/minilm) conçue par Microsoft. Entrainé pour la similarité sémantique et les recherches de phrases, ce modèle de 86 Mo est compact et optimisé pour offrir des performances élevées en termes de qualité d'encodage de phrases, tout en restant léger et rapide. Il semble parfait pour notre **chatbot** et la **recherche de similarité**.

Une fois le choix du modèle arrêté, ajoutons sa dépendance dans le pom.xml :

```xml
<dependency>
  <groupId>dev.langchain4j</groupId>
  <artifactId>langchain4j-embeddings-all-minilm-l6-v2</artifactId>
  <version>${langchain4j.version}</version>
</dependency>
```


Dans la classe de configuration Spring [AssistantConfiguration](https://github.com/spring-petclinic/spring-petclinic-langchain4j/blob/v3.3.3/src/main/java/org/springframework/samples/petclinic/chat/AssistantConfiguration.java), déclarons un bean de type [EmbeddingModel](https://docs.langchain4j.dev/tutorials/rag#embedding-model) :

```java
@Bean
EmbeddingModel embeddingModel() {
    return new AllMiniLmL6V2EmbeddingModel();
}
```


L’ingestion des données vétérinaires est réalisée en moins d’une seconde au démarrage de l’application Petclinic via la classe [EmbeddingStoreInit](https://github.com/spring-petclinic/spring-petclinic-langchain4j/blob/v3.3.3/src/main/java/org/springframework/samples/petclinic/chat/EmbeddingStoreInit.java) :

```java
@Component
public class EmbeddingStoreInit {

    private final Logger logger = LoggerFactory.getLogger(EmbeddingStoreInit.class);

    private final InMemoryEmbeddingStore<TextSegment> embeddingStore;

    private final EmbeddingModel embeddingModel;

    private final VetRepository vetRepository;

    public EmbeddingStoreInit(InMemoryEmbeddingStore<TextSegment> embeddingStore, EmbeddingModel embeddingModel,
          VetRepository vetRepository) {
       this.embeddingStore = embeddingStore;
       this.embeddingModel = embeddingModel;
       this.vetRepository = vetRepository;
    }

    @EventListener
    public void loadVetDataToEmbeddingStoreOnStartup(ApplicationStartedEvent event) {
       Pageable pageable = PageRequest.of(0, Integer.MAX_VALUE);
       Page<Vet> vetsPage = vetRepository.findAll(pageable);

       String vetsAsJson = convertListToJson(vetsPage.getContent());

       EmbeddingStoreIngestor ingestor = EmbeddingStoreIngestor.builder()
          .documentSplitter(new DocumentByLineSplitter(1000, 200))
          .embeddingModel(embeddingModel)
          .embeddingStore(embeddingStore)
          .build();

       ingestor.ingest(new Document(vetsAsJson));
    }

    public String convertListToJson(List<Vet> vets) {
       ObjectMapper objectMapper = new ObjectMapper();
       try {
          // Convert List<Vet> to JSON string
          StringBuilder jsonArray = new StringBuilder();
          for (Vet vet : vets) {
             String jsonElement = objectMapper.writeValueAsString(vet);
             jsonArray.append(jsonElement).append("\n"); // For use of the
                                              // DocumentByLineSplitter
          }
          return jsonArray.toString();
       }
       catch (JsonProcessingException e) {
          logger.error("Problems encountered when generating JSON from the vets list", e);
          return null;
       }
    }

}
```


La classe EmbeddingStoreInit fait appel au [_VetRepository_](https://github.com/spring-petclinic/spring-petclinic-langchain4j/blob/v3.3.3/src/main/java/org/springframework/samples/petclinic/vet/VetRepository.java) pour charger tous vétérinaires de la base, les marshalle en un gros [Document](https://github.com/langchain4j/langchain4j/blob/0.35.0/langchain4j-core/src/main/java/dev/langchain4j/data/document/Document.java) JSON puis fait appel à la classe [EmbeddingStoreIngestor](https://docs.langchain4j.dev/tutorials/rag/#embedding-store-ingestor) de LangChain4j. Ce EmbeddingStoreIngestor est configuré avec le modèle d’embedding, la base vectorielle où les embeddings seront stockés et un [DocumentByLineSplitter](https://github.com/langchain4j/langchain4j/blob/0.35.0/langchain4j/src/main/java/dev/langchain4j/data/document/splitter/DocumentByLineSplitter.java) chargé de découper le volumineux document JSON en [TextSegment](https://github.com/langchain4j/langchain4j/blob/0.35.0/langchain4j-core/src/main/java/dev/langchain4j/data/segment/TextSegment.java) censé améliorer la qualité des recherches de similarité et de réduire la taille et le coût d'une invite envoyée au LLM.

Une fois le EmbeddingStoreIngestor construit, la méthode **ingest()** est appelée pour ingérer le document. Comme le montre les logs ci-dessous, ce dernier est découpé en 33 segments de texte. Les embeddings sont calculés sur les 33 segments puis stockés dans la base vectorielle :

```text
EmbeddingStoreIngestor  : Starting to ingest 1 documents
EmbeddingStoreIngestor  : Documents were split into 33 text segments
EmbeddingStoreIngestor  : Starting to embed 33 text segments
EmbeddingStoreIngestor  : Finished embedding 33 text segments
EmbeddingStoreIngestor  : Starting to store 33 text segments into the embedding store
EmbeddingStoreIngestor  : Finished storing 33 text segments into the embedding store
```

## Requêtage des embeddings

A présent que l’ensemble des données vétérinaires sont stockées en base vectorielle sous forme d’embeddings, configurons l’application pour que le chatbot utilise ces données lors de son dialogue avec le LLM.

Pour utiliser les fonctionnalités RAG, la classe @AiService [Assistant](https://github.com/spring-petclinic/spring-petclinic-langchain4j/blob/v3.3.3/src/main/java/org/springframework/samples/petclinic/chat/Assistant.java) passe par l’interface [RetrievalAugmentor](https://docs.langchain4j.dev/tutorials/rag/#retrieval-augmentor) et [son implémentation par défaut](https://docs.langchain4j.dev/tutorials/rag/#default-retrieval-augmentor) mise à disposition par LangChain4j. Cette interface est chargée d’enrichir le _ChatMessage_ avec des contenus pertinents extraits d’une ou plusieurs sources de données, comme par exemple notre base vectorielle en mémoire. Pour avoir un aperçu des composants manipulés par le RetrievalAugmentor, je vous invite à consulter le [schéma du paragraphe Advanced RAG](https://docs.langchain4j.dev/tutorials/rag/#advanced-rag) de la documentation de LangChain4j. On y voit l’utilisation d’un [ContentRetriever](https://docs.langchain4j.dev/tutorials/rag/#content-retriever) pour interroger une base vectorielle, un moteur de recherche, une base SQL ou bien encore un moteur de recherche.

Dans Petclinic, nous déclarons un bean ContentRetriever de type [EmbeddingStoreContentRetriever](EmbeddingStoreContentRetriever) chargé de récupérer des données vétérinaires dans notre base vectorielle :

```java
@Bean
EmbeddingStoreContentRetriever contentRetriever(InMemoryEmbeddingStore<TextSegment> embeddingStore,
       EmbeddingModel embeddingModel) {
    return new EmbeddingStoreContentRetriever(embeddingStore, embeddingModel);
}
```


En redémarrant l’application Petclinic puis en posant une question au chatbot, on s’aperçoit que LangChain4j complète le prompt de l’utilisateur en concaténant à la suite de sa question la liste des vétérinaires issus de la base vectorielle et qui se rapprochent sémantiquement de sa question :

```text
- method: POST
- url: https://api.openai.com/v1/chat/completions
- headers: [Accept: text/event-stream], [Authorization: Bearer xxx], [User-Agent: langchain4j-openai]
- body: {
  "model" : "gpt-4o",
  "messages" : [ {
    "role" : "system",
    "content" : "You are a friendly AI assistant …"
  }, {
    "role" : "user",
    "content" : "\"I'm looking for a veterinarian who specializes in both radiography and odontology for my pet \"\n\ content Answer using the following information:\n{\"id\":158,\"firstName\":\"Lauren\",\"lastName\":\"Wood\",\"new\":false,\"specialties\":[{\"id\":2,\"name\":\"surgery\",\"new\":false}]}\n{\"id\":159,\"firstName\":\"Gary\",\"lastName\":\"Coleman\",\"new\":false,\"specialties\":[{\"id\":1,\"name\":\"radiology\",\"new\":false},{\"id\":2,\"name\":\"surgery\",\"new\":false}]}\ …"
  } ],
  "temperature" : 0.7, … }

```

## Routage de questions

Le dernier point présenté dans cet article consiste à utiliser la fonctionnalité **[Query Router](https://docs.langchain4j.dev/tutorials/rag/#query-router)** de LangChain4j. Interroger la base vectorielle pour chaque question n’a pas nécessairement d’intérêt. Par exemple pour un simple « Hello » ou une question portant uniquement sur les propriétaires.  
Comme son nom le laisse supposer, un Query Router est **responsable de router une requête utilisateur vers le ou les ContentRetriever appropriés** **si nécessaire**.

L’implémentation de l’interface [QueryRouter](https://github.com/langchain4j/langchain4j/blob/0.35.0/langchain4j-core/src/main/java/dev/langchain4j/rag/query/router/QueryRouter.java) est à la charge du développeur. Pour déterminer si la question d’un utilisateur porte sur les vétérinaires, on aurait pu utiliser une simple recherche de la chaine de caractère « vet ». D’une part, on n’aurait pas supporter le multilingue et d’autre part on aurait interrogé la base vectorielle si l’utilisateur nous avait posé une question hors contexte sur, par exemples, les vétérans. **Qui mieux qu’un LLM peut déterminer la sémantique de la question ?**  
La classe [VetQueryRouter](https://github.com/spring-petclinic/spring-petclinic-langchain4j/blob/v3.3.3/src/main/java/org/springframework/samples/petclinic/chat/VetQueryRouter.java) fait un premier appel au LLM pour répondre à la question  « Is the following query related to one or more veterinarians of the pet clinic? ». On demande au LLM de répondre par oui ou par non. Sé réponse détermine si l’usage du Embedding Store est nécessaire. Nul besoin ici d’utiliser de streaming.

```java
class VetQueryRouter implements QueryRouter {

    private static final Logger LOGGER = LoggerFactory.getLogger(VetQueryRouter.class);

    private static final PromptTemplate PROMPT_TEMPLATE = PromptTemplate.from("""
          Is the following query related to one or more veterinarians of the pet clinic?
          Answer only 'yes' or 'no'.
          Query: {{it}}
          """);

    private final ContentRetriever vetContentRetriever;

    private final ChatLanguageModel chatLanguageModel;

    public VetQueryRouter(ChatLanguageModel chatLanguageModel, ContentRetriever vetContentRetriever) {
       this.chatLanguageModel = chatLanguageModel;
       this.vetContentRetriever = vetContentRetriever;
    }

    @Override
    public Collection<ContentRetriever> route(Query query) {
       Prompt prompt = PROMPT_TEMPLATE.apply(query.text());

       AiMessage aiMessage = chatLanguageModel.generate(prompt.toUserMessage()).content();
       LOGGER.debug("LLM decided: {}", aiMessage.text());

       if (aiMessage.text().toLowerCase().contains("yes")) {
          return singletonList(vetContentRetriever);
       }
       return emptyList();
    }
}
```


La déclaration du VetQueryRouter au niveau de [AssistantConfiguration](https://github.com/spring-petclinic/spring-petclinic-langchain4j/blob/v3.3.3/src/main/java/org/springframework/samples/petclinic/chat/AssistantConfiguration.java) passe par l’utilisation de la méthode builder de la classe _DefaultRetrievalAugmentor_ :

```java
@Bean
RetrievalAugmentor retrievalAugmentor(ChatLanguageModel chatLanguageModel, ContentRetriever vetContentRetriever) {
    return DefaultRetrievalAugmentor.builder()
       .queryRouter(new VetQueryRouter(chatLanguageModel, vetContentRetriever))
       .build();
}
```


Petclinic utilisant désormais le _ChatLanguageModel_ et le _StreamingChatLanguageModel_, le fichier de configuration application.properties doit être complété :

```properties
langchain4j.open-ai.streaming-chat-model.api-key=${OPENAI_API_KEY}
langchain4j.open-ai.streaming-chat-model.model-name=gpt-4o
langchain4j.open-ai.streaming-chat-model.log-requests=true
langchain4j.open-ai.streaming-chat-model.log-responses=true
langchain4j.open-ai.chat-model.api-key=${OPENAI_API_KEY}
langchain4j.open-ai.chat-model.model-name=gpt-4o-mini
langchain4j.open-ai.chat-model.log-requests=true
langchain4j.open-ai.chat-model.log-responses=true
```

Dans les logs applicatifs, un premier appel est désormais envoyé au LLM avant toute autre appel :

```text
- method: POST
- url: https://api.openai.com/v1/chat/completions
- headers: [Authorization: Bearer sk-Qw...MA], [User-Agent: langchain4j-openai]
- body: {
  "model" : "gpt-4o-mini",
  "messages" : [ {
    "role" : "user",
    "content" : "Is the following query related to one or more veterinarians of the pet clinic?\nAnswer only 'yes' or 'no'.\nQuery: \"I'm looking for a veterinarian who specializes in both radiography and odontology for my pet \"\n"
  } ],
  "temperature" : 0.7
}

```

## Conclusion

Cet article aura montré comment intégrer LangChain4j dans une application de gestion basée sur Spring Boot.

Récapitulons les principales fonctionnalités de LangChain4j qui ont été mises en œuvre :

1. **AI Service**: définit de manière déclarative l’interface entre notre application Java et un LLM.
1. **Memory** : permet d’historiser les conversations entre l’utilisateur et le LLM, supporte le multi-utilisateurs et la persistance.
1. **System prompt** : joue un rôle essentiel dans les LLM car il détermine la manière dont les modèles interprètent les requêtes des utilisateurs et y répondent.
1. **Tooling**(ou **appel de fonction**) : permet au LLM d'appeler, si nécessaire, une ou plusieurs méthodes Java de l’application.
1. **Streaming** : réponse au fil de l’eau, token par token, en utilisant côté client le Server-Sent Events.
1. **RAG**: utilisation d’un embedding store en mémoire pour ingérer les données vétérinaires, faire des recherches de similarité et enrichir le prompt utilisateur en fonction d’une règle de routage.

Personnellement, le développement de la version LangChain4j de Spring Petclinic m’aura permis de contribuer modestement au projet Open Source LangChain4j (PR [#49](https://github.com/langchain4j/langchain4j-spring/pull/49), [#50](https://github.com/langchain4j/langchain4j-spring/pull/50), [#51](https://github.com/langchain4j/langchain4j-spring/pull/51) et # [2000](https://github.com/langchain4j/langchain4j/pull/2000)).

Je tiens à remercier mon fils Evan pour son [montage de ma video Youtube](https://youtu.be/hy2HDMjLr_8). Merci également à Antonio Goncalves, Julien Dubois, Guillaume Laforge et Valentin Deleplace pour leurs workshops sur LangChain4j avec [Azure OpenAI](https://moaw.dev/workshop/?src=gh:Azure-Samples/azure-openai-rag-workshop-java/docs/workshop-java-quarkus.md) et [Gemini](https://devfest2024.gdgnantes.com/sessions/hands_on_gemini_with_java_and_langchain4j_on_vertex_ai/).

Si vous souhaitez contribuez à votre tour à [Spring Petclinic LangChain4j](https://github.com/spring-petclinic/spring-petclinic-langchain4j), des [issues](https://github.com/spring-petclinic/spring-petclinic-langchain4j/issues) vous attendent. L’ [issue #10](https://github.com/spring-petclinic/spring-petclinic-langchain4j/issues/10) vise notamment à intégrer d’autres LLM que OpenAI et Azure OpenAI. Parmi les candidats potentiels figurent Google Vertex AI Gemini, Ollama ou bien encore Mistral AI. Avis aux amatrices et aux amateurs.

Ressources :

- [Documentation officielle LangChain4j](https://docs.langchain4j.dev/)
- Repository Git [spring-petclinic-langchain4j](https://github.com/spring-petclinic/spring-petclinic-langchain4j)
- [AI Meets Spring Petclinic: Implementing an AI Assistant with Spring AI](https://spring.io/blog/2024/09/26/ai-meets-spring-petclinic-implementing-an-ai-assistant-with-spring-ai-part-i) (Oded Shopen)
- [OpenAI Developer Quickstart](https://platform.openai.com/docs/quickstart))
- [Java client library for OpenAI API](https://github.com/ai-for-java/openai4j)
- [Gemini en Java avec Vertex AI et LangChain4j](https://codelabs.developers.google.com/codelabs/gemini-java-developers) (Google Lab)
- [Create your own ChatGPT with Retrieval-Augmented-Generation](https://moaw.dev/workshop/?src=gh:Azure-Samples/azure-openai-rag-workshop-java/docs/workshop-java-quarkus.md) (Microsoft)
