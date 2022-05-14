import { useEffect, useState } from 'react';
import styled from 'styled-components';

const Home = () => {
  const [channels, setChannels] = useState([]);

  useEffect(() => {
    (async () => {
      const receivedChannels = await fetch('http://127.0.0.1:5000/videos').then(
        (res) => res.json()
      );
      setChannels(receivedChannels);
    })();
  }, []);

  return (
    <>
      {channels.map(({ channel: { name, id }, videos }) => (
        <ChannelContainer key={id}>
          <h3>{name}</h3>
          <VideosContainer>
            {videos.map((video) => (
              <VideoItem>
                <LinkWrapper
                  href={'https://www.youtube.com/watch?v=' + video.id}
                  target="_blank"
                >
                  <Thumbnail src={video.thumbnail} />
                  <span>{video.title}</span>
                </LinkWrapper>
              </VideoItem>
            ))}
          </VideosContainer>
        </ChannelContainer>
      ))}
    </>
  );
};

export default Home;

const ChannelContainer = styled.div`
  padding: 10px;
`;

const VideosContainer = styled.div`
  width: 100%;
  overflow-x: auto;
  white-space: nowrap;
  overflow-y: hidden;
`;

const VideoItem = styled.div`
  display: inline-block;
  vertical-align: top;
  white-space: break-spaces;
  margin: 0 10px 0 0;
  width: 220px;
`;

const Thumbnail = styled.img`
  width: 100%;
  display: block;
`;

const LinkWrapper = styled.a`
  &:any-link {
    color: black;
    text-decoration: none;
  }
`;
