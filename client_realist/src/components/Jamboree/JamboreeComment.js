import React from 'react'
import { Comment, Icon } from 'semantic-ui-react'

const JamboreeComment = ({author,text}) => (
    <Comment>
      <Comment.Avatar as='a' src={`http://api.adorable.io/avatars/50/${author}`} />
      <Comment.Content>
        <Comment.Author>{author}</Comment.Author>
        <Comment.Text>
            {text}
        </Comment.Text>
      </Comment.Content>
    </Comment>
)

export default JamboreeComment;