FROM openjdk:8-jdk-alpine
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} redis.jar
ENTRYPOINT ["java","-jar","/redis.jar"]