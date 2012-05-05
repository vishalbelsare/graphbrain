organization := "com.graphbrain"

name := "webapp"

version := "0.1.0-SNAPSHOT"

scalaVersion := "2.9.1"

scalacOptions += "-deprecation"

scalacOptions += "-unchecked"

fork in run := true

resolvers ++= Seq("Coda Hales Repository" at "http://repo.codahale.com")

libraryDependencies ++= Seq(
  "net.databinder" %% "unfiltered-netty-server" % "0.5.3",
  "net.databinder" %% "dispatch-nio" % "0.8.8",
  "org.clapper" %% "avsl" % "0.3.6",
  "net.databinder" %% "unfiltered-spec" % "0.5.3" % "test",
  "org.scalatest" %% "scalatest" % "1.7.1" % "test",
  "com.codahale" %% "jerkson" % "0.5.0",
  "com.codahale" %% "logula" % "2.1.3"
)